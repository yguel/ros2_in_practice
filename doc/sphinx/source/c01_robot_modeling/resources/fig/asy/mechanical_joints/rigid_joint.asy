pen nice_yellow = rgb(255,160,0);

path[][] rigid_joint() {
    path p1_1,p1_2,p2;
    pair a,b,c,d;
    a = (-2,0);
    b = (2,-1);
    p1_1 = a -- b;
    c = 0.5*(b-a)+a;
    d = (1,1);
    real start,end;
    start = degrees(b-a);
    end = degrees(a-b);
    p1_2 = arc((0,0), 0.27, start, end, CCW) -- (0,0) -- cycle;
    path[] left = {p1_1,shift(b+0.27*unit((a-b)))*p1_2};

    p2 = c -- d;
    path[] right = {p2};

    path[][] res = {left,right};

    return res;
}

void draw_rigid_joint(pen left_p=squarecap + black, pen right_p=squarecap+nice_yellow,picture pic=currentpicture){
    path[][] left_right;
    left_right = rigid_joint();
    fill(pic, left_right[0][1],left_p);
    draw(pic, left_right[1],right_p);
    draw(pic, left_right[0][0],left_p);
}

void draw_rigid_logo(string filename, string format="svg"){
    // Begin a new picture
    currentpicture = new picture;
    unitsize(1cm);

    draw_rigid_joint(
        left_p = squarecap+black+3, 
        right_p = squarecap+nice_yellow+3,
        pic=currentpicture);

    // Draw rigid motion
    label(scale(2)*"$\emptyset$", (0,-1.2), black+3 );

    // Save the current picture
    shipout(prefix=filename, pic=currentpicture, format=format);
}

draw_rigid_logo("rigid_joint_logo");
exit();