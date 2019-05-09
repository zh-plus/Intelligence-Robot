sim = ExampleHelperRobotSimulator('simpleMap');
setRobotPose(sim, [2 3 -pi/2]);% Enable ROS interface for the simulator. The simulator
% creates publishers and subscribers to send and receive data over ROS.
enableROSInterface(sim, true);
% Increase the laser sensor resolution in the simulator to
% facilitate map building.
sim.LaserSensor.NumReadings = 50;

scanSub = rossubscriber('scan');
[velPub, velMsg] = rospublisher('/mobile_base/commands/velocity');

tftree = rostf;
% Pause for a second for the transformation tree object to finish
% initialization.
pause(1);

path = [2, 3;3.25 6.25;2 11;6 7; 11 11;8 6; 10 5;7 3;11 1.5];
plot(path(:,1), path(:,2),'k--d')

controller = robotics.PurePursuit('Waypoints', path);
controller.DesiredLinearVelocity = 0.4;
controlRate = robotics.Rate(10);
goalRadius = 0.1;
robotCurrentLocation = path(1,:);
robotGoal = path(end,:);
distanceToGoal = norm(robotCurrentLocation -robotGoal);

map = robotics.OccupancyGrid(14,13,20);
figureHandle = figure('Name', 'Map');
axesHandle = axes('Parent', figureHandle);
mapHandle = show(map, 'Parent', axesHandle);
title(axesHandle, 'OccupancyGrid: Update 0');

map.FreeThreshold = 0.5;
map.OccupiedThreshold = 0.5;

updateCounter = 1;
while( distanceToGoal > goalRadius )
    % Receive a new laser sensor reading
    scanMsg = receive(scanSub);
    
    % Get robot pose at the time of sensor reading
    pose = getTransform(tftree, 'map', 'robot_base', scanMsg.Header.Stamp, 'Timeout', 2);
    % Convert robot pose to1x3 vector [x y yaw]
    position = [pose.Transform.Translation.X,pose.Transform.Translation.Y];
    orientation =  quat2eul([pose.Transform.Rotation.W,pose.Transform.Rotation.X, ...
        pose.Transform.Rotation.Y, pose.Transform.Rotation.Z], 'ZYX');
    robotPose = [position, orientation(1)];
    
    % Extract the laser scan
    scan = lidarScan(scanMsg);
    ranges = scan.Ranges;
    ranges(isnan(ranges)) = sim.LaserSensor.MaxRange;
    modScan = lidarScan(ranges, scan.Angles);
    
    % Insert the laser range observation in the map
    insertRay(map, robotPose,modScan, sim.LaserSensor.MaxRange);

    % Compute the linear and angular velocity of the robot and publish it
    % to drive the robot.
    [v, w] = controller(robotPose);
    velMsg.Linear.X = v;
    velMsg.Angular.Z = w;
    send(velPub, velMsg);
    % Visualize the map after every 50th update.
    if~mod(updateCounter,50)
        mapHandle.CData = occupancyMatrix(map);
        title(axesHandle, ['OccupancyGrid: Update ' num2str(updateCounter)]);
    end

    % Update the counter and distance to goal
    updateCounter = updateCounter+1;
    distanceToGoal = norm(robotPose(1:2) -robotGoal);
    % Wait for control rate to ensure 10 Hz rate
    waitfor(controlRate);
end

show(map, 'Parent', axesHandle);
title(axesHandle, 'OccupancyGrid: Final Map');

insertRay(map, robotPose, modScan, sim.LaserSensor.MaxRange);

% initialize alpha and beta accumulators
alpha= zeros(map.GridSize);
beta = zeros(map.GridSize);

% Insert the laser range observation in the map 
for n = 1:modScan.Count
    [endpoints, midpoints] = raycast(map, robotPose,modScan.Ranges(n), ...
        modScan.Angles(n));
    if modScan.Ranges(n) == sim.LaserSensor.MaxRange
        beta = elementAdd(beta, endpoints);
    else
        alpha = elementAdd(alpha, endpoints);
    end
    beta = elementAdd(beta, midpoints);
    setij = [midpoints ; endpoints];
    [m, nc] = size(setij);
    occup = zeros(m, 1);
    for i = 1:m
        occup(i) = alpha(setij(i,1), setij(i,2)) / ...
            (alpha(setij(i,1), setij(i,2)) + beta(setij(i,1),setij(i,2)));
    end
setOccupancy(map, setij, occup, 'grid');
end

function matrix = elementAdd(matrix, addij)
%elementAdd Add 1 at specified elements of 'matrix'
%   Add 1 at each elements of 'matrix' specified by index vector 'addij'.
[m, n] = size(addij);
for i = 1:m
    matrix(addij(i,1), addij(i,2)) = matrix(addij(i,1), addij(i,2)) + 1;
end
end
