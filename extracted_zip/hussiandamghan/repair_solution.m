function position = repair_solution(position,desired_features)

idx1 = find(position==1);
idx0 = find(position==0);

if length(idx1) > desired_features
    
    remove = randperm(length(idx1),length(idx1)-desired_features);
    position(idx1(remove)) = 0;
    
elseif length(idx1) < desired_features
    
    add = randperm(length(idx0),desired_features-length(idx1));
    position(idx0(add)) = 1;
    
end

end
