

type_high = 0.914;
relief = 1/8;


scale(25.4) translate([-1/4, 1/16, 0]) linear_extrude(height = type_high) scale(1/100 * [1, 1, 1]) import("MCChop.svg");
scale(25.4) cube([1 + 3/8, 2, type_high - relief]);
