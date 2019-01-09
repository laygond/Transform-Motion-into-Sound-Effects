clear; close all;
% target port as set in the app
port        = 5555;
payloadData = cell(1000,1);
% Initializing data
data1 = 0;
data2 = 0;
data3 = 0;
sq_data = 0;
% Figure plotting starts
figure;
 for k=1:4000
   % get the message/payload only assuming a max size of 200 bytes
   [msg,~] = judp('RECEIVE',port,200);
   % save the payload to the array
   payloadData{k} = msg;
   
   % Create a CSV file and keep updating it with data values
   fileID = fopen('exp.csv','w');
   fprintf(fileID,'%s\n',double(msg(1:end-1))');
   fclose(fileID);
   M(k,:) = csvread('exp.csv'); % Put CSV values into columns of a matrix
   
   % Appending data points for plotting 
   data1 = [data1 M(k,7)];
   data2 = [data2 M(k,8)];
   data3 = [data3 M(k,9)];
   sq(k) = sqrt(M(k,1)^2 + M(k,3)^2); 
   sq_data = [sq_data sq(k)];
   
   % Plotting real time plots of sensors
   subplot(4,1,1)
   plot(data1, 'LineWidth', 2)
   title('Sensor Values')
   subplot(4,1,2)
   plot(data2, 'LineWidth', 2)
   title('X axis')
   subplot(4,1,3)
   plot(data3, 'LineWidth', 2)
   title('Y axis')
   subplot(4,1,4)
   plot(sq_data, 'LineWidth', 2)
   title('Z axis')
   pause(.0000001)
end