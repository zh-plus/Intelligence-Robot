[x,y] = meshgrid(-1.2:0.2:1.2, -1.2:0.2:1.2);
shape = size(x);
distance = sqrt(x.^2 + y.^2)
a = (distance > 0.3)
constants = (distance > 0.3) .* ones(shape)