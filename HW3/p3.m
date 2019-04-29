clear;
clc;

%% =========== satellites position =======
sate = [
    14000 12000 18000;
    90000 21000 15000;
    12000 6000 19000
    ];

%% =========== user position s1, s2, s3 (x, y, z) =======
user = [4000 3000 1000];

scatter3(user(1), user(2), user(3));
hold on;
scatter3(sate(: ,1), sate(: ,2), sate(: ,3), 'filled');

p_distance = calculate_psudo_distance(sate, user);
cal_user = calculate_user_position(sate, p_distance)
scatter3(cal_user(1), cal_user(2), cal_user(3));

function [distance] = calculate_distance(sate, user)
diff = sate - user;
distance = sum(diff.*diff, 2) .^(0.5);
end

function [p_distance] = calculate_psudo_distance(sate, user)
distance = calculate_distance(sate, user);
p_distance = sum(distance.*distance, 2) .^(0.5) + 5000;
end

function diff = F(x, sate, p_range)
diff = calculate_distance(x, sate) - p_range;
end

function [cal_user] = calculate_user_position(sate, p_range)
[x,~] = fsolve(@(x) F(x, sate, p_range),[0,0,0]);
cal_user = x;
end