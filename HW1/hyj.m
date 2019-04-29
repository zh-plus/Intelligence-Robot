function mobile_robot_NN()
clc
close all
clear all

%% =========== Set the paramters =======
T=0.01; % Sampling Time
k=2; % Sampling counter
x(k-1)=0.7; % initilize the state x
y(k-1)=0.8; % initilize the state y
theta(k-1)=0; % initilize the state theta
tfinal=100; % final simulation time
t=0; % intilize the time
height=-0.8; % the height of rectangle in perpendicular field
%=====================================


%% ============== Main =================
run_in_uniform_field();
% run_in_perpendicular_field()
%run_in_attractive_field()
%run_in_repulsive_field()
%run_in_tangential_field()
%=====================================


%% =========== Draw Field =============
    function draw_uniform_field()
        [a,b] = meshgrid(-1.2:0.2:1.2,-1.2:0.2:1.2);
        u = ones(length(a));
        v = 0*a;

        quiver(a,b,u,v,0.5)
    end

    function draw_perpendicular_field()
        [a,b] = meshgrid(-1.2:0.2:1.2,-1.2:0.2:1.2);
        u = 0*a;
        v = ones(length(a));
        
        r = rectangle('Position', [-1.2, height-0.1, 2.4, 0.1]);
        r.FaceColor = [0 0 0];
        
        for i = 1:length(b)
            for j = 1:length(b(i,:))
                if b(i,j) < height
                    v(i,j) = 0;
                end
            end
        end
        quiver(a,b,u,v,0.5)
    end

    function draw_attractive_field()
        [a,b] = meshgrid(-1.2:0.2:1.2,-1.2:0.2:1.2);
        u = -a;
        v = -b;

        quiver(a,b,u,v,0.7)
    end

    function draw_repulsive_field()
        [a,b] = meshgrid(-1.2:0.2:1.2,-1.2:0.2:1.2);
        u = a;
        v = b;

        quiver(a,b,u,v,0.7)
    end

    function draw_tangential_field()
        [a,b] = meshgrid(-1.2:0.2:1.2,-1.2:0.2:1.2);
        hypotenuse = sqrt((a.^2 + b.^2));
        u = b ./ hypotenuse;
        v = -a ./ hypotenuse;

        quiver(a,b,u,v,0.7)
    end
%=====================================

%% =========== The main loop ==========
    function run_in_uniform_field()
        while(t<=tfinal)
            t=t+T; % increase the time
            V=0.5;
            theta(k)=0;
            x(k)=V*cos(theta(k))*T+x(k-1); % calculating x
            y(k)=V*sin(theta(k))*T+y(k-1); % calculating y
            
            draw_robot(); % Draw the robot and it's path
            draw_uniform_field();     
            drawnow
            hold off
            
            k=k+1; % increase the sampling counter
        end
    end

    function run_in_perpendicular_field()
        while(t<=tfinal)
            t=t+T; % increase the time
            V=0.5;
            theta(k)=pi/2; % calculating theta
            if y(k-1) > height
                x(k)=V*cos(theta(k))*T+x(k-1); % calculating x
                y(k)=V*sin(theta(k))*T+y(k-1); % calculating y
            else
                x(k)=x(k-1);
                y(k)=y(k-1);
            end
            
            draw_robot(); % Draw the robot and it's path
            draw_perpendicular_field();
            drawnow
            hold off
            
            k=k+1; % increase the sampling counter
        end
    end

    function run_in_attractive_field()
        while(t<=tfinal)
            t=t+T; % increase the time
            V=1;
            V=(x(k-1)^2 + y(k-1)^2) * V;
            if x(k-1) > 0
                offset = pi;
            else
                offset = 0;
            end
            theta(k)=atan(y(k-1)/x(k-1))+offset; % calculating theta
            x(k)=V*cos(theta(k))*T+x(k-1); % calculating x
            y(k)=V*sin(theta(k))*T+y(k-1); % calculating y
            
            draw_robot(); % Draw the robot and it's path
            draw_attractive_field();
            drawnow
            hold off
            
            k=k+1; % increase the sampling counter
        end
    end

    function run_in_repulsive_field()
        while(t<=tfinal)
            t=t+T; % increase the time
            V=1;
            V=(x(k-1)^2 + y(k-1)^2) * V;
            if x(k-1) > 0
                offset = 0;
            else
                offset = pi;
            end
            theta(k)=atan(y(k-1)/x(k-1))+offset; % calculating theta
            x(k)=V*cos(theta(k))*T+x(k-1); % calculating x
            y(k)=V*sin(theta(k))*T+y(k-1); % calculating y
            
            draw_robot(); % Draw the robot and it's path
            draw_repulsive_field();
            drawnow
            hold off
            
            k=k+1; % increase the sampling counter
        end
    end

    function run_in_tangential_field()
        while(t<=tfinal)
            t=t+T; % increase the time
            V=1;
            V=(x(k-1)^2 + y(k-1)^2) * V;
            if x(k-1) > 0
                offset = pi;
            else
                offset = 0;
            end
            theta(k)=atan(y(k-1)/x(k-1))+offset+pi/2; % calculating theta
            x(k)=V*cos(theta(k))*T+x(k-1); % calculating x
            y(k)=V*sin(theta(k))*T+y(k-1); % calculating y
            
            draw_robot(); % Draw the robot and it's path
            draw_tangential_field();
            drawnow
            hold off
            
            k=k+1; % increase the sampling counter
        end
    end

%=====================================

%% === Draw the mobile robot & Path ====
    function draw_robot()
        xmin=-1.2; % setting the figure limits
        xmax=1.2;
        ymin=-1.2;
        ymax=1.2;
        mob_L=0.2; % The Mobile Robot length
        mob_W=0.1; % The Mobile Robot width
        Tire_W=0.05; % The Tire width
        Tire_L=mob_L/2;  % The Tire length
        plot(x,y,'-r') % Dawing the Path
        axis([xmin xmax ymin ymax]) % setting the figure limits
        axis square
        hold on
        
        % Body
        v1=[mob_L;-mob_W];
        v2=[-mob_L/4;-mob_W];
        v3=[-mob_L/4;mob_W];
        v4=[mob_L;mob_W];
        %Right Tire
        v5=[Tire_L/2;-mob_W-0.02];
        v6=[Tire_L/2;-mob_W-Tire_W-0.02];
        v7=[-Tire_L/2;-mob_W-Tire_W-0.02];
        v8=[-Tire_L/2;-mob_W-0.02];
        %Left Tire
        v9=[Tire_L/2;mob_W+0.02];
        v10=[Tire_L/2;mob_W+Tire_W+0.02];
        v11=[-Tire_L/2;mob_W+Tire_W+0.02];
        v12=[-Tire_L/2;mob_W+0.02];
        %Line
        v13=[0;-mob_W-0.02];
        v14=[0;mob_W+0.02];
        %Front Tire
        v15=[mob_L;Tire_W/2];
        v16=[mob_L;-Tire_W/2];
        v17=[mob_L-Tire_L/1.5;-Tire_W/2];
        v18=[mob_L-Tire_L/1.5;Tire_W/2];
        
        R=[cos(theta(k)) -sin(theta(k));sin(theta(k)) cos(theta(k))]; % Rotation Matrix
        P=[x(k);y(k)]; % Position Matrix
        
        v1=R*v1+P;
        v2=R*v2+P;
        v3=R*v3+P;
        v4=R*v4+P;
        
        v5=R*v5+P;
        v6=R*v6+P;
        v7=R*v7+P;
        v8=R*v8+P;
        
        v9=R*v9+P;
        v10=R*v10+P;
        v11=R*v11+P;
        v12=R*v12+P;
        
        v13=R*v13+P;
        v14=R*v14+P;
        
        v15=R*v15+P;
        v16=R*v16+P;
        v17=R*v17+P;
        v18=R*v18+P;
        
        
        %Body
        mob_x=[v1(1) v2(1) v3(1) v4(1) v1(1)];
        mob_y=[v1(2) v2(2) v3(2) v4(2) v1(2)];
        plot(mob_x,mob_y,'-k','linewidth',2)
        
        %Right Tire
        mob_x=[v5(1) v6(1) v7(1) v8(1) v5(1)];
        mob_y=[v5(2) v6(2) v7(2) v8(2) v5(2)];
        plot(mob_x,mob_y,'-k','linewidth',2)
        fill(mob_x,mob_y,'b')
        
        %Left Tire
        mob_x=[v9(1) v10(1) v11(1) v12(1) v9(1)];
        mob_y=[v9(2) v10(2) v11(2) v12(2) v9(2)];
        plot(mob_x,mob_y,'-k','linewidth',2)
        fill(mob_x,mob_y,'b')
        
        %Line Between tires
        mob_x=[v13(1) v14(1)];
        mob_y=[v13(2) v14(2)];
        plot(mob_x,mob_y,'-k','linewidth',3)
        
        %Front tire
        mob_x=[v15(1) v16(1) v17(1) v18(1) v15(1)];
        mob_y=[v15(2) v16(2) v17(2) v18(2) v15(2)];
        plot(mob_x,mob_y,'-k','linewidth',1)
        fill(mob_x,mob_y,'b')

    end
%=====================================



end