% https://www.mathworks.com/help/matlab/ref/imwrite.html

filepath = 'D:\Monash\FIT3162\GIF collection\levi.gif';
[gifImage map] = imread(filepath, 'gif' ,'Frames', 'all');

newimagename = 'D:\Monash\FIT3162\GIF collection\levi2.gif';
imwrite(gifImage, map, newimagename);