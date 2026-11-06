clc;
clear;
close all;
%% Load Data
data = readmatrix('spambase.xlsx');

X = data(:,1:end-1);
Y = data(:,end);

[nSamples,nFeatures] = size(X);

%% Normalization
X = (X - min(X))./(max(X)-min(X)+eps);

%% Train Test Split
cv = cvpartition(Y,'HoldOut',0.2);

Xtrain = X(training(cv),:);
Ytrain = Y(training(cv));

Xtest = X(test(cv),:);
Ytest = Y(test(cv));

%% Parameters
desired_features = 47;
MaxIt = 20;
nPop = 10;

%% Run Algorithm
[BestSol,BestCost] = GA_PSO_feature_selection( ...
    Xtrain,Ytrain,nPop,MaxIt,nFeatures,desired_features);

selected_features = find(BestSol.Position);

fprintf('\nSelected Features:\n');
disp(selected_features)

%% Train Final Model
model = TreeBagger(100,...
    Xtrain(:,selected_features),...
    Ytrain,...
    'Method','classification');

%% Prediction

[pred, Yscore] = predict(model,Xtest(:,selected_features));

pred = str2double(pred);

%% Accuracy

accuracy = sum(pred==Ytest)/length(Ytest);

fprintf('\nFinal Test Accuracy = %.4f\n',accuracy);
%% Plot Results

plot_results(BestCost,Ytest,pred,Yscore)
