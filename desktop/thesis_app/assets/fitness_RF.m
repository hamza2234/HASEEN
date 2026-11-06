function cost = fitness_RF(position,Xtrain,Ytrain,desired_features)

features = find(position);

if isempty(features)
    cost = 1;
    return
end

model = TreeBagger(50,Xtrain(:,features),Ytrain,'Method','classification');

pred = predict(model,Xtrain(:,features));
pred = str2double(pred);

accuracy = sum(pred==Ytrain)/length(Ytrain);

feature_penalty = abs(length(features)-desired_features)/desired_features;

cost = 1 - accuracy + 0.01*feature_penalty;

end
