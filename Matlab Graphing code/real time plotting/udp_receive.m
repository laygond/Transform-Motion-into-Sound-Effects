
% target port as set in the app
 port        = 5555;
 payloadData = cell(1000,1);
data1 = 0;
data2 = 0;
data3 = 0;
figure;
 for k=1:4000
   % get the message/payload only assuming a max size of 200 bytes
   [msg,~] = judp('RECEIVE',port,200);
   % save the payload to the array
   payloadData{k} = msg;
   % convert the message to ASCII and print it out
   
   fileID = fopen('exp.csv','w');
   fprintf(fileID,'%s\n',double(msg(1:end-1))');
   fclose(fileID);
   M(k,:) = csvread('exp.csv');
   
   
   
    
   data1 = [data1 abs(M(k,7))];
   data2 = [data2 abs(M(k,8))];
   data3 = [data3 abs(M(k,9))];
   subplot(3,1,1)
   plot(data1)
   title('x axis')
   subplot(3,1,2)
   plot(data2)
   title('y axis')
   subplot(3,1,3)
   plot(data3)
   title('z axis')
   pause(.0000001)
    

   
 end