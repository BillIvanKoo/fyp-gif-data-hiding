% https://www.mathworks.com/help/matlab/ref/imwrite.html

filepath = 'D:\Monash\FIT3162\GIF collection\levi.gif';
[gifImage map] = imread(filepath, 'gif' ,'Frames', 'all');

% get information of a file
% https://www.mathworks.com/help/matlab/ref/imfinfo.html
info = imfinfo(filepath);
% info.DelayTime returns the delay time (fps) in hundredths of seconds
% returned value should be divided by 100 (to make it into seconds)
ans = info.DelayTime;
fps = ans / 100;

newimagename = 'D:\Monash\FIT3162\GIF collection\levi2.gif';
imwrite(gifImage, map, newimagename,'gif','LoopCount',Inf,'DelayTime',fps);
%imwrite(A,map,filename,'gif','LoopCount',Inf,'DelayTime',1);
fprintf("gif generated\n");