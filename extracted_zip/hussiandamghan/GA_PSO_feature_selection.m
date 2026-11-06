function [GlobalBest,BestCost] = GA_PSO_feature_selection( ...
    Xtrain,Ytrain,nPop,MaxIt,nVar,desired_features)

%% Parameters
w = 0.7;
c1 = 1.5;
c2 = 1.5;

mutation_rate = 0.2;

empty_particle.Position = [];
empty_particle.Velocity = [];
empty_particle.Cost = [];
empty_particle.BestPosition = [];
empty_particle.BestCost = [];

pop = repmat(empty_particle,nPop,1);

GlobalBest.Cost = inf;

%% Initialization
for i=1:nPop
    
    pos = zeros(1,nVar);
    idx = randperm(nVar,desired_features);
    pos(idx)=1;
    
    pop(i).Position = pos;
    pop(i).Velocity = zeros(1,nVar);
    
    pop(i).Cost = fitness_RF(pos,Xtrain,Ytrain,desired_features);
    
    pop(i).BestPosition = pos;
    pop(i).BestCost = pop(i).Cost;
    
    if pop(i).BestCost < GlobalBest.Cost
        GlobalBest = pop(i);
    end
    
end

BestCost = zeros(MaxIt,1);

%% Main Loop
for it=1:MaxIt
    
    for i=1:nPop
        
        r1 = rand(1,nVar);
        r2 = rand(1,nVar);
        
        %% PSO Velocity
        pop(i).Velocity = ...
            w*pop(i).Velocity ...
            + c1*r1.*(pop(i).BestPosition - pop(i).Position) ...
            + c2*r2.*(GlobalBest.Position - pop(i).Position);
        
        %% Position Update
        pop(i).Position = pop(i).Position + pop(i).Velocity;
        
        pop(i).Position = 1./(1+exp(-pop(i).Position));
        pop(i).Position = pop(i).Position > rand(size(pop(i).Position));
        
        %% Repair
        pop(i).Position = repair_solution(pop(i).Position,desired_features);
        
        %% Evaluation
        pop(i).Cost = fitness_RF(pop(i).Position,Xtrain,Ytrain,desired_features);
        
        %% Update Personal Best
        if pop(i).Cost < pop(i).BestCost
            
            pop(i).BestCost = pop(i).Cost;
            pop(i).BestPosition = pop(i).Position;
            
            %% Update Global Best
            if pop(i).BestCost < GlobalBest.Cost
                GlobalBest = pop(i);
            end
            
        end
        
    end
    
    %% GA Crossover
    for k=1:round(nPop/4)
        
        i1 = randi(nPop);
        i2 = randi(nPop);
        
        parent1 = pop(i1).Position;
        parent2 = pop(i2).Position;
        
        alpha = rand;
        
        child = alpha*parent1 + (1-alpha)*parent2;
        child = child > 0.5;
        
        child = repair_solution(child,desired_features);
        
        child_cost = fitness_RF(child,Xtrain,Ytrain,desired_features);
        
        worst = randi(nPop);
        
        if child_cost < pop(worst).Cost
            
            pop(worst).Position = child;
            pop(worst).Cost = child_cost;
            pop(worst).BestPosition = child;
            pop(worst).BestCost = child_cost;
            
        end
        
    end
    
    %% Mutation
    for i=1:nPop
        
        if rand < mutation_rate
            
            j = randi(nVar);
            pop(i).Position(j) = 1 - pop(i).Position(j);
            
            pop(i).Position = repair_solution(pop(i).Position,desired_features);
            
            pop(i).Cost = fitness_RF(pop(i).Position,Xtrain,Ytrain,desired_features);
            
        end
        
    end
    
    BestCost(it) = GlobalBest.Cost;
    
    fprintf('Iteration %d BestCost %.5f Features %d\n',...
        it,GlobalBest.Cost,sum(GlobalBest.Position));
    
end

end
