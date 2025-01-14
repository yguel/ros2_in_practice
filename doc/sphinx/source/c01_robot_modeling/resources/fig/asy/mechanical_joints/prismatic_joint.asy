pen nice_yellow = rgb(255,160,0);

path[][] prismatic_joint(real delta=1, real sep=0.05) {
    path p1_1,p1_2,p1_3,p2_1,p2_2;
    p1_1 = (-1,0) -- (0,0);
    p1_2 = (1.5,-1)--(0,-1)--(0,1)--(1.5,1);
    p1_3 = arc((0,0), 0.27, 180, 90) -- (0,0) -- cycle;
    path[] left = {p1_1,p1_2,p1_3};

    real ssep = 1-sep;
    p2_1 = (0,-ssep)--(0,ssep);
    p2_2 = (0,0)--(1.5,0);

    path[] right = {p2_1,p2_2};

    path[][] res = {left,shift((delta,0))*right};

    return res;
}

void draw_prismatic_joint(real delta=0.8, real sep=0.05, pen left_p=squarecap + black, pen right_p=squarecap+nice_yellow,picture pic=currentpicture){
    path[][] left_right;
    left_right = prismatic_joint(delta,sep);
    draw(pic, left_right[0][0],left_p);
    draw(pic, left_right[0][1],left_p);
    fill(pic, left_right[0][2],left_p);
    draw(pic, left_right[1],right_p);
}

path prismatic_motion(){
    return shift(-0.5,-1.5)*( (0,0)--(1.75,0) );
}

void draw_prismatic_motion(pen p=squarecap + black,real arrow_size=3mm, picture pic=currentpicture){
    draw(pic, prismatic_motion(),p,arrow=Arrows(size=arrow_size));
}

void draw_prismatic_logo(string filename, string format="svg"){
    // Begin a new picture
    currentpicture = new picture;
    unitsize(1cm);

    draw_prismatic_joint(sep=0.15, 
        left_p = squarecap+black+3, 
        right_p = squarecap+nice_yellow+3,
        pic=currentpicture);
    draw_prismatic_motion(p=squarecap+black+2,pic=currentpicture);

    // Save the current picture
    shipout(prefix=filename, pic=currentpicture, format=format
    );
}

draw_prismatic_logo("prismatic_joint_logo");
exit();