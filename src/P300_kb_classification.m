function [answer,results,nStims,targets] = P300_kb_classification(all_signals, all_states, all_parameters, channels, wmap, hp, epochLength, thresh,nPart,nTrain,lambda)

signal=all_signals{1};
if(nargin < 4)
    channels=ones(size(signal,2),1);
end;
%channels(mean(abs(cell2mat(all_signals)))>200)=0;

mapflag=1;
if(nargin < 5)
    mapflag=0;
end;

hpflag=1;
if(or(nargin < 6,hp==0))
    hpflag=0;
end;

parameters=all_parameters{1};
nr=parameters.NumMatrixColumns.NumericValue;
nc=parameters.NumMatrixRows.NumericValue;
rate = parameters.SamplingRate.NumericValue;
if(nargin < 7)
    epochLength = parameters.EpochLength.NumericValue;
end;
epochPoints = ceil(epochLength * rate / 1000);
if(nargin < 8)
    thresh = [1,.999999999,.99999999,.9999999,.999999,.99999,.9999,.999,.998,.997,.995,.99,.98,.97,.96,.95,.94,.93,.92,.91,.9,.85,.8,.75,.7,.65,.6,.55,.5,.4,.3,.2,.1,0];
end;
if(nargin < 9)
    nPart = 1000;
end;

trainflag=1;
if nargin < 10
    trainflag=0;
end;

if(nargin < 11)
    lambda=0;
end;

DSFactor = 12;
downsampleFunc =@ DownSampleMatByAvg;
%downsampleFunc =@ DownSampleMatByAPCA;
%downsampleFunc =@ DownSampleMatByPivot;
nAvgTrial = 1;

stimFlag1 = false;
stimFlag2 = false;
try
    states=all_states{1};
    states.StimulusCode1;
    stimFlag1 = true;
    try
        states.StimulusCode3;
        stimFlag2 = true;
    catch e2
        'states does not contain StimulusCode3'
    end;
catch e1
    'states does not contain StimulusCode1'
end;


allLabels=[];
allStim=[];
allStim1=[];
allStim2=[];
allStim3=[];
allData=[];
allNStim=[];
allNLetters=[];
for iter = 1:length(all_signals)
    sprintf('file number %d\n',iter)
    signal=double(all_signals{iter}(:,channels==1));
    if(hpflag)
        [num,den]=butter(1,hp/(rate/2),'high');
        signal=filter(num,den,signal);
    end;
    states=all_states{iter};
    parameters=all_parameters{iter};
    
    stimulusType = states.StimulusType;
    stimulusCode = double(states.StimulusCode);
    
    if(stimFlag1)
        stimulusCode1 = double(states.StimulusCode1);
        stimulusCode2 = double(states.StimulusCode2);
    else
        stimulusCode1 = zeros(size(stimulusCode));
        stimulusCode2 = zeros(size(stimulusCode));
    end;
    if(stimFlag2)
        stimulusCode3 = double(states.StimulusCode3);
    else
        stimulusCode3 = zeros(size(stimulusCode));
    end;
    
    stimulusCode1(stimulusCode==circshift(stimulusCode,1))=0;
    stimulusCode2(stimulusCode==circshift(stimulusCode,1))=0;
    stimulusCode3(stimulusCode==circshift(stimulusCode,1))=0;
    stimulusCode(stimulusCode==circshift(stimulusCode,1))=0;
    onsetIndices = find(stimulusCode>0);
    word=lower(parameters.TextToSpell.Value{1});
    
    ends=[1;find(and(states.PhaseInSequence==3,circshift(states.PhaseInSequence,1)~=3))];
    onsetIndices=onsetIndices(onsetIndices<ends(end));
    tNStim=zeros(length(ends)-1,1);
    for i=2:length(ends)
        tNStim(i-1)=sum(and(onsetIndices>ends(i-1),onsetIndices<ends(i)));
    end;
    onsetIndices=onsetIndices(1:sum(tNStim));
    
    allLabels = [allLabels;double(stimulusType(onsetIndices))];
    allStim  = [allStim;stimulusCode(onsetIndices)];
    allStim1 = [allStim1;stimulusCode1(onsetIndices)];
    allStim2 = [allStim2;stimulusCode2(onsetIndices)];
    allStim3 = [allStim3;stimulusCode3(onsetIndices)];
    allNStim = [allNStim;tNStim];
    allNLetters = [allNLetters;length(word)];
    
    for i=1:length(onsetIndices)
        temp=DownSample4Feature(signal(onsetIndices(i):(onsetIndices(i)+epochPoints-1),:),DSFactor,nAvgTrial,[],downsampleFunc);
        allData=[allData,temp(:)];
    end;
end;


answer = cell(length(all_signals),1);
results= cell(length(all_signals),length(thresh));
nStims = cell(length(all_signals),length(thresh));

counter=1;
index=1;
for i=1:length(all_signals)
    fprintf('Training file %d\n',i)
    fileLength=size(allData,2)/length(all_signals);
    testIndices=(i-1)*fileLength+(1:fileLength);
    trainData=allData(:,setdiff(1:size(allData,2),testIndices));
    trainLabels=allLabels(setdiff(1:size(allData,2),testIndices));
    trainStim=allStim(setdiff(1:size(allData,2),    testIndices));
    
    ind=max(abs(trainData),[],1)<200;
    trainData=trainData(:,ind);
    trainLabels=trainLabels(ind);
    
    indices=randperm(length(trainLabels));
    if(trainflag)
        indices=indices(1:nTrain);
    end;
    
    trainData1=trainData(:,indices);
    trainLabels1=trainLabels(indices);
    [coeff1,feaSelector1]=BuildStepwiseLDA(trainData1',trainLabels1);
    if(~isempty(coeff1))
        attScore1=min(1,max(-1,trainData1(feaSelector1,find(trainLabels1==1))'*coeff1));
        nonScore1=min(1,max(-1,trainData1(feaSelector1,find(trainLabels1~=1))'*coeff1));
    else
        attScore1=normrnd(0,1,sum(trainLabels1==1),1);
        nonScore1=normrnd(0,1,sum(trainLabels1~=1),1);
    end;
    attMean=mean(attScore1);
    nonMean=mean(nonScore1);
    attSD=std(attScore1);
    nonSD=std(nonScore1);
    
    TestSet = i;
    fprintf('Testing file %d\n',i)
    for j=TestSet
        parameters=all_parameters{j};
        word=strrep(lower(parameters.TextToSpell.Value{1}),' ','_');
        answer{j}=zeros(1,allNLetters(j));
        temp=parameters.TargetDefinitions.Value(:,1);
        for k=1:length(temp)
            if(strcmp(temp{k},'sp'))
                temp{k}='_';
            end;
            if(length(temp{k})>1)
                temp{k}='0';
            end;
            try 
                wmap.(['x' temp{k}])=0;
            catch
                temp{k}='0';
            end;
        end;
        targets = lower(cell2mat(temp));
        
        pStrings=ones(nPart,length(thresh),allNLetters(j));
        for k=1:length(thresh)
            nStims{j,k}=zeros(allNLetters(j),1);
        end;
        for k=1:allNLetters(j)
            fprintf('Testing letter %d for file %d\n',k,i)
            answer{j}(k)=targets(targets==word(k));
            fprintf(['Target character: ' char(answer{j}) '\n'])
            
            nStim=ones(length(thresh),1)*(-1);
            priorProbs=zeros(nPart,length(thresh),length(targets));
            for l=1:nPart
                for m=1:length(thresh)
                    tstring=['_' targets(pStrings(l,m,1:(k-1)))'];
                    tstring=tstring((find(tstring=='_',1,'last')+1):end);
                    for n=1:length(targets)
                        if ~isfield(wmap,['t' tstring targets(n)])
                            wmap.(['t' tstring targets(n)])=0;
                        end;
                        if ~isfield(wmap,['t' tstring])
                            wmap.(['t' tstring])=0;
                        end;
                        if wmap.(['t' tstring])>-lambda*length(targets)
                            priorProbs(l,m,n)=priorProbs(l,m,n)+log10(wmap.(['t' tstring targets(n)])+lambda)...
                                -log10(wmap.(['t' tstring])+lambda*length(targets));
                        else
                            priorProbs(l,m,n)=log10(0);
                        end;
                    end;
                    priorProbs(l,m,:)=priorProbs(l,m,:)-log10(sum(power(10,priorProbs(l,m,:))));
                end;
            end;
            priorCDFs=zeros(nPart,length(thresh));
            priorRands=rand(nPart,length(thresh));
            priorProj=ones(nPart,length(thresh))*length(targets);
            for l=1:length(targets)
                priorCDFs=priorCDFs+power(10,priorProbs(:,:,l));
                priorProj(and(priorProj==length(targets),priorCDFs>priorRands))=l;
            end;
            for l=1:nPart
                for m=find(nStim<0)'
                    pStrings(l,m,k)=priorProj(l,m);
                end;
            end;
            postProbs=-log10(nPart)*ones(nPart,length(thresh));
            %resample (only if exceeds thresh without data)
            for l=find(nStim<0)'
                for m=1:length(targets)
                    if sum(power(10,postProbs(priorProj(:,l)==m,l)))>thresh(l)
                        %sprintf('thresh: %d, target: %d, iteration: %d',l,m,0)
                        nStim(l)=0;
                        nStims{j,l}(k)=0;
                        postCDFs=0;
                        postRands=rand(nPart,1);
                        postProj=zeros(nPart,1);
                        for n=1:nPart
                            postCDFs=postCDFs+power(10,postProbs(n,l));
                            postProj(and(postProj==0,(ones(nPart,1)*postCDFs)>postRands))=n;
                        end;
                        pStrings(:,l,:)=pStrings(postProj,l,:);
                        break;
                    end;
                end;
            end;

            targetProbs=zeros(length(targets),1);
            targetProbs2=zeros(length(targets),allNStim(counter));
            for l=1:allNStim(counter)
                %index
                score=min(1,max(-1,allData(feaSelector1,index)'*coeff1));
                temp=fliplr([dec2bin(allStim3(index),32),dec2bin(allStim2(index),32),dec2bin(allStim1(index),32)]);
                for m=1:length(targets)
                    row=floor((m-1)/nc)+1;
                    col=mod(m-1,nc)+1+nr;
                    if or(and(or(allStim(index)==row,allStim(index)==col),~stimFlag1),and(temp(m)=='1',stimFlag1))
                        targetProbs(m)=targetProbs(m)+log10(normpdf(score,attMean,attSD))-log10(normpdf(score,nonMean,nonSD));
                        %postProbs(:,:,m)=postProbs(:,:,m)+log10(normpdf(score,attMean,attSD))-log10(normpdf(score,nonMean,nonSD));
                        %postProbs(priorProj==m)=postProbs(priorProj==m)+log10(normpdf(score,attMean,attSD))-log10(normpdf(score,nonMean,nonSD));
                    end;
                end;
                targetProbs=targetProbs-log10(sum(power(10,targetProbs)));
                targetProbs2(:,l)=targetProbs;
                for m=1:length(targets)
                    postProbs(priorProj==m)=targetProbs(m);
                end;
                postProbs=postProbs-log10(ones(nPart,1)*sum(power(10,postProbs),1));
                %resample
                for m=find(nStim<0)'
                    for n=1:length(targets)
                        if or(sum(power(10,postProbs(priorProj(:,m)==n,m)))>thresh(m),and(l==allNStim(counter),n==length(targets)))
                            %sprintf('thresh: %d, target: %d, iteration: %d',m,n,l)
                            nStim(m)=l;
                            nStims{j,m}(k)=l;
                            postCDFs=0;
                            postRands=rand(nPart,1);
                            postProj=zeros(nPart,1);
                            for o=1:nPart
                                postCDFs=postCDFs+power(10,postProbs(o,m));
                                postProj(and(postProj==0,(ones(nPart,1)*postCDFs)>postRands))=o;
                            end;
                            pStrings(:,m,:)=pStrings(postProj,m,:);
                            break;
                        end;
                    end;
                end;
                index=index+1;
            end;
            counter=counter+1;
            for l=1
                result=[];
                for m=1:nPart
                    try
                        result.(['t' targets(pStrings(m,l,:))'])=result.(['t' targets(pStrings(m,l,:))'])+1/nPart;
                    catch e
                        result.(['t' targets(pStrings(m,l,:))'])=1/nPart;
                    end;
                end;
                result
            end;
        end;
        for l=1:length(thresh)
            result=[];
            for m=1:nPart
                try
                    result.(['t' targets(pStrings(m,l,:))'])=result.(['t' targets(pStrings(m,l,:))'])+1/nPart;
                catch e
                    result.(['t' targets(pStrings(m,l,:))'])=1/nPart;
                end;
            end;
            results{j,l}=result;
        end;
    end;
end;

