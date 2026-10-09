# Prespecified GLMM/LMM; diagnostics control interpretation, never p-value selection.
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==2)
suppressPackageStartupMessages(library(lme4))
library(jsonlite)
d <- read.csv(args[1],stringsAsFactors=FALSE)
d$composition <- factor(d$composition,levels=c('unbounded','bounded'))
d$knowledge <- factor(d$knowledge,levels=c('real','nonce','micro'))
d$context <- factor(d$context,levels=c('neutral','supportive','cancelling'))
d$stratum <- factor(d$stratum);d$template <- factor(d$template)
d$family_id <- factor(d$family_id);d$verb <- factor(d$verb);d$model <- factor(d$model)
d$prior <- factor(d$prior,levels=c('low','high'))
d$bounded_num <- as.numeric(d$composition=='bounded')
reports <- list()
attempt <- function(formula,dat,kind,label) {
 warnings <- character();fit <- NULL;error <- NULL
 fit <- tryCatch(withCallingHandlers({
  if(kind=='binary') glmer(formula,data=dat,family=binomial(),nAGQ=1,control=glmerControl(optimizer='bobyqa',optCtrl=list(maxfun=20000)))
  else lmer(formula,data=dat,REML=FALSE,control=lmerControl(optimizer='bobyqa',optCtrl=list(maxfun=20000)))
 },warning=function(w){warnings<<-c(warnings,conditionMessage(w));invokeRestart('muffleWarning')}),error=function(e){error<<-conditionMessage(e);NULL})
 if(is.null(fit))return(list(label=label,formula=deparse(formula),n=nrow(dat),usable=FALSE,error=error,warnings=unique(warnings)))
 cc <- as.data.frame(coef(summary(fit)));cc$term <- rownames(cc);rownames(cc)<-NULL
 conv <- fit@optinfo$conv$lme4$messages
 optimizer_code <- fit@optinfo$conv$opt
 optimizer_ok <- !is.null(optimizer_code) && all(optimizer_code==0)
 dropped <- attr(getME(fit,'X'),'col.dropped')
 cc$ci95_wald_lower <- cc$Estimate-1.96*cc$`Std. Error`
 cc$ci95_wald_upper <- cc$Estimate+1.96*cc$`Std. Error`
 finite <- all(is.finite(fixef(fit))) && all(is.finite(cc$`Std. Error`))
 # Extreme logit coefficients / standard errors diagnose near-separation, not significance.
 unstable <- kind=='binary' && (any(abs(fixef(fit))>20) || any(cc$`Std. Error`>100))
 singular <- isSingular(fit,tol=1e-4)
 list(label=label,formula=deparse(formula),n=nrow(dat),usable=finite && !unstable && !singular && is.null(conv) && optimizer_ok && length(warnings)==0 && is.null(dropped),optimizer_return_code=optimizer_code,singular=singular,near_separation_numeric_flag=unstable,convergence_messages=conv,warnings=unique(warnings),dropped_columns=names(dropped),coefficients=cc,random_variances=as.data.frame(VarCorr(fit)),logLik=as.numeric(logLik(fit)),AIC=AIC(fit),estimator=if(kind=='binary')'maximum likelihood, Laplace nAGQ=1' else 'Gaussian maximum likelihood, raw q')
}
fit_pair <- function(dat,outcome,kind,extra='',label) {
 fixed <- paste(outcome,'~ composition * knowledge * context + stratum + template',extra)
 full <- as.formula(paste(fixed,'+ (1 + bounded_num | family_id) + (1 | verb)'))
 a <- attempt(full,dat,kind,paste0(label,'_full'))
 fits <- list(a)
 if(!isTRUE(a$usable))fits[[2]] <- attempt(as.formula(paste(fixed,'+ (1 | family_id) + (1 | verb)')),dat,kind,paste0(label,'_intercepts_fallback'))
 list(fits=fits,final_usable=isTRUE(tail(fits,1)[[1]]$usable),reporting=if(isTRUE(tail(fits,1)[[1]]$usable))'secondary model coefficients; primary inference remains paired cluster contrasts' else 'No model-based inferential claim; use exact cell proportions and prespecified paired cluster contrasts')
}
for(mid in levels(d$model)) {
 core <- subset(d,model==mid & dataset=='main_core')
 if(nrow(core)!=2160)stop('All planned core rows required, including missing correctness.')
 result <- list(binary=fit_pair(core,'correct','binary',label='correct'))
 qdata <- core[is.finite(core$q),]
 result$q <- if(nrow(qdata))fit_pair(qdata,'q','linear',label='q') else list(final_usable=FALSE,reason='no valid q')
 prior <- subset(d,model==mid & dataset=='main_prior' & is.finite(q))
 result$intended_prior <- if(nrow(prior))attempt(q~prior*context+template+(1|family_id)+(1|verb),prior,'linear','exploratory_intended_prior') else list(usable=FALSE,reason='no valid intended-prior q')
 reports[[mid]] <- result
}
combined <- subset(d,dataset=='main_core')
reports$combined_correct <- attempt(correct~composition*knowledge*context+model*composition*knowledge+model*context+stratum+template+(1+bounded_num|family_id)+(1|verb),combined,'binary','combined_fixed_named_systems')
scale <- subset(d,dataset=='main_core' & model %in% c('qwen/qwen3-8b','qwen/qwen3-14b','qwen/qwen3-32b') & is.finite(q))
sizes <- c('qwen/qwen3-8b'=8.2,'qwen/qwen3-14b'=14.8,'qwen/qwen3-32b'=32.8)
scale$log2_size <- log2(unname(sizes[as.character(scale$model)]))
reports$qwen_scale <- attempt(q~log2_size*composition+log2_size*knowledge+context+stratum+template+(1+bounded_num|family_id)+(1|verb),scale,'linear','within_qwen_association')
write_json(list(session_info=capture.output(sessionInfo()),lme4_version=as.character(packageVersion('lme4')),R_version=R.version.string,scope='secondary conditional operational models, no human validation',model_reports=reports),args[2],pretty=TRUE,auto_unbox=TRUE,na='null')
