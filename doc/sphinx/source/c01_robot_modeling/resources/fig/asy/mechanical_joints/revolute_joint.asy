pen nice_yellow = rgb(255,160,0);

path[][] revolute_joint(real radius=0.8, real angle_deg=25) {
    path p1_1,p1_2,p1_3,p2;
    real k = 2.75;
    p1_1 = scale(radius)*unitcircle;
    p1_2 = (0,-radius)--(0,-k*radius);
    p1_3 = arc((0,0), 0.27, 175, 270) -- (0,0) -- cycle;
    path[] left = {p1_1,p1_2,shift(0,-radius)*p1_3};

    p2 = rotate(angle_deg)*((radius,0)--(k*radius,0));

    path[] right = {p2};

    path[][] res = {left,right};

    return res;
}

void draw_revolute_joint(pen left_p=squarecap + black, pen right_p=squarecap+nice_yellow,picture pic=currentpicture){
    path[][] left_right;
    left_right = revolute_joint();
    draw(pic, left_right[1],right_p);
    draw(pic, left_right[0][0],left_p);
    draw(pic, left_right[0][1],left_p);
    fill(pic, left_right[0][2],left_p);
}

path revolute_motion(real radius=1.5, real angle_deg=25){
    real k = 0.5*radius;
    return shift(k,-k)*( arc((0,0), radius, -90, angle_deg) );
}

void draw_revolute_motion(pen p=squarecap + black,real arrow_size=2.5mm, picture pic=currentpicture){
    draw(pic, revolute_motion(),p,arrow=Arrows(size=arrow_size));
}

void draw_revolute_logo(string filename, string format="svg"){
    // Begin a new picture
    currentpicture = new picture;
    unitsize(1cm);

    draw_revolute_joint(
        left_p = squarecap+black+5, 
        right_p = squarecap+nice_yellow+5,
        pic=currentpicture);
    draw_revolute_motion(p=squarecap+black+2,pic=currentpicture);

    // Save the current picture
    shipout(prefix=filename, pic=currentpicture, format=format);
}

draw_revolute_logo("revolute_joint_logo");




