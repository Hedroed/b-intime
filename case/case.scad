$fa = 1;
$fs = 0.4;

module inner() {
    c_w = 6;
    c_h = 18;

    color("orangered") cube([136, 16, 67]);
    
    color("grey") translate([-20+0.01, 5, 8]) cube([20, c_w, c_h]);
    color("grey") translate([-20+0.01, 5, 67-8-c_h]) cube([20, c_w, c_h]);
    color("grey") translate([136-0.01, 5, 8]) cube([20, c_w, c_h]);
};

module screen() {
    color("lightblue") cube([126, 10, 67]);
}

module screw(o=0) {
    translate([1.5,0,1.5]) rotate([90,0,0])
        cylinder(50, d=3, center=true);
    color("green")
        translate([1.5,1.99,1.5]) rotate([90,o,0])
        cylinder(d=6, h=2, $fn=5);
    color("red")
        translate([1.5,20.01,1.5]) rotate([90,0,0])
        cylinder(h = 1.5, r1 = 2, r2 = 1, center = false);
}

module inner2() {
    translate([2.5,0,2.5])
        screw(35);
    translate([150-5,0,71-5])
        screw();
    translate([2.5,0,71-5])
        screw(35);
    translate([150-5,0,2.5])
        screw();
    
    translate([2+5,2,2])
        inner();
    translate([5+5+2,16,2])
        screen();
}


//translate([0,-200,0]) inner2();

module boite() {
    
    difference() {
        cube([150,20,71]);
        inner2();
    }
}

difference() {
    union() {
        boite();
        translate([0, 20, 150]) rotate([180,0,0]) boite();
    };
    translate([-1,10,-1]) cube([400, 11, 400]);
}


