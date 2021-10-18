


module octahedron() {
    
     octo_points = [
        [0, -1, 0], // belt
        [ 1, 0, 0], 
        [ 0,  1, 0], 
        [-1,  0, 0], 
        [0, 0, 1], // top
        [0, 0, -1], // bottom
    ];

    octo_faces = [
        [0, 1, 4], // top pyramid
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        [1, 0, 5], // bottom pyramid
        [2, 1, 5],
        [3, 2, 5],
        [0, 3, 5],
    ];

    polyhedron(
        points = octo_points,
        faces = octo_faces
    );
}



module octoflake(i, size, center){
    
    if (i == 0){
        translate(center) scale(size) octahedron();
    } else {
        octoflake(i-1, size/2, center + 1/2 * size * [0, -1, 0]);
        octoflake(i-1, size/2, center + 1/2 * size * [1, 0, 0]);
        octoflake(i-1, size/2, center + 1/2 * size * [0, 1, 0]);
        octoflake(i-1, size/2, center + 1/2 * size * [-1, 0, 0]);
        octoflake(i-1, size/2, center + 1/2 * size * [0, 0, 1]);
        octoflake(i-1, size/2, center + 1/2 * size * [0, 0, -1]);
    }
    
    
}




octoflake(2, 1, [0,0,0]);