flist=dir('images/*.jpg');

img_list=cell(length(flist),1);
for f=1:length(flist)
    img_list{f}=['images/' flist(f).name];
end
    
flist=dir('annotations/*.png');
annotation_list=cell(length(flist),1);
annotation_id=cell(length(flist),1);
for f=1:length(flist)
    annotation_list{f}=['annotations/' flist(f).name];
    annotation_id{f}  =flist(f).name(1:4);
end


for f=1:length(img_list)
    f
    close all
    img_add=img_list{f};
    anno_adds=annotation_list(strcmp(img_add(8:11), annotation_id));
    
    for k=1:length(anno_adds)
        anno_add=anno_adds{k};
        anno=imread(anno_add);
        
        
        figure(k)
        imshow(anno*12) % change anno range from 0-19 to 0-228 for better visualization        
        colormap default
                
    end
    
    img=imread(img_add);  
    figure(100)    
    imshow(img)
    
    pause
end
        
    
    
