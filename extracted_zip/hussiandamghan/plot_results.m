function plot_results(BestCost, Ytest, Ypred, Yscore)

%% ============================================================
%  1. GA-PSO Convergence Plot
% ============================================================
figure
plot(BestCost,'LineWidth',2)
xlabel('Iteration','FontSize',12)
ylabel('Best Cost','FontSize',12)
title('GA-PSO Convergence Curve','FontSize',14)
grid on
set(gca,'FontSize',12)


%% ============================================================
% 2. Confusion Matrix
% ============================================================
figure
cm = confusionchart(Ytest, Ypred);
cm.Title = 'Confusion Matrix (Test Data)';
cm.FontSize = 12;


%% ============================================================
% 3. ROC Curve
% ============================================================

% اگر TreeBagger احتمال دوکلاسی دهد، ستون دوم کلاس مثبت است
if size(Yscore,2)==2
    score = Yscore(:,2);
else
    score = Yscore;
end

[Xroc, Yroc, ~, AUC] = perfcurve(Ytest, score, max(Ytest));

figure
plot(Xroc, Yroc,'LineWidth',2)
hold on
plot([0 1],[0 1],'k--')
xlabel('False Positive Rate','FontSize',12)
ylabel('True Positive Rate','FontSize',12)
title(['ROC Curve (AUC = ' num2str(AUC,'%.3f') ')'],'FontSize',14)
grid on
set(gca,'FontSize',12)


%% ============================================================
% 4. Performance Metrics Bar Plot
% ============================================================

% confusion matrix برای محاسبه دقیق
C = confusionmat(Ytest, Ypred);

TP = C(2,2);
TN = C(1,1);
FP = C(1,2);
FN = C(2,1);

accuracy = (TP + TN) / sum(C(:));
precision = TP / (TP + FP + eps);
recall = TP / (TP + FN + eps);
f1 = 2 * (precision * recall) / (precision + recall + eps);

metrics = [accuracy precision recall f1] * 100;

figure
b = bar(metrics, 'FaceColor',[0 0.447 0.741]);
ylabel('Percentage (%)','FontSize',12)
set(gca,'XTickLabel',{'Accuracy','Precision','Recall','F1-score'})
title('Performance Metrics (Test Data)','FontSize',14)
ylim([0 100])
grid on
set(gca,'FontSize',12)

% نمایش مقدار درصد روی هر میله
for i = 1:length(metrics)
    text(i, metrics(i)+1, sprintf('%.2f%%',metrics(i)), ...
        'HorizontalAlignment','center','FontSize',11);
end


%% چاپ متریک‌ها برای تطبیق با خروجی
disp('====== Confusion Matrix ======')
disp(C)

fprintf('\nAccuracy  = %.2f %%\n', metrics(1))
fprintf('Precision = %.2f %%\n', metrics(2))
fprintf('Recall    = %.2f %%\n', metrics(3))
fprintf('F1-score  = %.2f %%\n\n', metrics(4))

end
