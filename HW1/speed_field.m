%% =========== The main loop ==========
uniform_field();
% perpendicular_field();
% attractive_field();
% repulsive_field();
% tengrential_field();
%=====================================


%% === Uniform field ====
    function uniform_field()
        [x,y] = meshgrid(-1.2:0.2:1.2, -1.2:0.2:1.2);
        shape = size(x);
        u = ones(shape) * 0.01;
        v = zeros(shape);
        
        figure
        quiver(x, y, u, v);
    end
%=====================================

%% === Perpendicular field ====
    function perpendicular_field()
        [x,y] = meshgrid(-1.2:0.2:1.2, -1.2:0.2:1.2);
        shape = size(x);
        u = zeros(shape);
        v = ones(shape) * 0.01;

        figure
        hold all
        quiver(x, y, u, v);
        rectangle('Position',[-1.5,-1.5,3,0.5],'facecolor',[0.1,0.2,0.3]);
    end
    
%=====================================


%% === Attractive field ====
    function attractive_field()
        [x,y] = meshgrid(-1.2:0.2:1.2, -1.2:0.2:1.2);
        center = [0 0];
        u = -x;
        v = -y;

        figure
        hold all
        quiver(x, y, u, v);
        plot(center(1), center(2),'.r','MarkerSize',50);
    end
%=====================================

%% === Repulsive field ====
    function repulsive_field()
        [x,y] = meshgrid(-1.2:0.2:1.2, -1.2:0.2:1.2);
        center = [0 0];
        u = x;
        v = y;

        figure
        hold all
        quiver(x, y, u, v);
        plot(center(1), center(2),'.r','MarkerSize',50);
    end
%=====================================

%% === Tengrential field ====
    function tengrential_field()
        [x,y] = meshgrid(-1.2:0.2:1.2, -1.2:0.2:1.2);
        center = [0 0];
        shape = size(x);
        u = y;
        v = -x;

        figure
        hold all
        quiver(x, y, u, v);
        plot(center(1), center(2),'.r','MarkerSize',50);
    end
%=====================================