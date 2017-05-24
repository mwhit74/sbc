import math

def shear(bolts, force):
    """Calculate the direct shear force in each direction on each bolt.

    For each bolt the force in the x and y directions is divided by total number
    of bolts and the resultant reaction is stored as the x and y reaction for
    each bolt.

    rx = px/num_bolts
    ry = py/num_bolts

    Args:
        bolts (list): List of the bolts in the connetion conforming to the
                        prescribed data structure for a bolt
        force (data struct): Data structure using a list to hold the force
                                attributes
    Returns:
        None
    """
    num_bolts = len(bolts)
    for bolt in bolts:
        px = force[1][0]
        py = force[1][1]

        rx = -px/num_bolts
        ry = -py/num_bolts

        bolt[4][0] = rx
        bolt[4][1] = ry

def tension(bolts, force):
    pass

def ecc_in_plane_elastic(bolts, force):
    """Calc the bolt reactions in an elastic in plane eccentric shear connection.
    
    For each bolt the moment about the z-axis is proportioned based the
    distance from the centroid of the group to center of the bolt. The resultant
    reaction is stored in the x and y force for each bolt. See Salmon and
    Johnson 5th Edition pp. 118 for further details. 

    rx = -1*mz*local_yb/j
    ry = mz*local_xb/j

    The rx is multiplied by -1 due to the coordinate system used for this program. 

    Args:
        bolts (list): List of the bolts in the connetion conforming to the
                        prescribed data structure for a bolt
        force (data struct): Data structure using a list to hold the force
                                attributes
    Returns:
        None

    """
    mz = force[2][2]

    j = calc_j(bolts)

    for bolt in bolts:
        local_xb = bolt[3][0]
        local_yb = bolt[3][1]

        #px = py*local_xf*local_yb/j - px*local_yf*local_yb/j
        #py = py*local_xf*local_xb/j - px*local_yf*local_xb/j
        rx = mz*local_yb/j
        ry = -1*mz*local_xb/j

        bolt[4][0] = rx
        bolt[4][1] = ry

def ecc_in_plane_plastic(bolts, force):
    pass

def calc_moments(bolts, force):
    """Calculate the x, y, and z moments.

    mx = pz(y) - py(z)
    my = px(z) - pz(x)
    mz = py(x) - px(y)

    Args:
        force (data struct): Data structure using a list to hold the force
                                attributes
    Returns:
        None
    """
    local_x = force[3][0]
    local_y = force[3][1]
    local_z = force[3][2]

    px = force[1][0]
    py = force[1][1]
    pz = force[1][2]

    mx = pz*local_y - py*local_z
    my = px*local_z - pz*local_x
    mz = py*local_x - px*local_y

    force[2][0] = mx
    force[2][1] = my
    force[2][2] = mz

def calc_plastic_instanteous_center(bolts):
    pass

def calc_elastic_instanteous_center_diff(bolts, force):
    """Calculate x and y distance of the elastic IC from the centroid."""
    j = calc_j(bolts)
    #calc_moments(force)

    num_bolts = len(bolts)

    px = force[1][0]
    py = force[1][1]
    mz = force[2][2]

    ax = -py/num_bolts*j/mz
    ay = px/num_bolts*j/mz

    return ax, ay

def calc_elastic_coeff(bolts):

def calc_d_eic(bolts, force):
    """Calculate the distance from the bolt to the elastic instanteous center."""
    ax, ay = calc_elastic_instanteous_center_diff(bolts, force)  

    for bolt in bolts:
      x = bolt[3][0] - ax
      y = bolt[3][1] - ay

      de = math.sqrt(math.pow(x,2) + math.pow(y,2))
      
      bolt[5] = de

def calc_mp(force):
    calc force coords about ic
    calc moment about ic

def calc_neutral_axis(bolts):
    pass

def calc_centroid(bolts):
    """Calculate the centroid of the bolt group."""
    sum_x = 0.0
    sum_y = 0.0
    num_bolts = len(bolts)
    for bolt in bolts:
        x = bolt[1][0]
        y = bolt[1][1]
        sum_x = sum_x + x
        sum_y = sum_y + y

    return sum_x/num_bolts, sum_y/num_bolts

def calc_local_bolt_coords(bolts):
    """Calculate bolt coords with the centroid of the bolt group as the origin."""
    x_cent, y_cent = calc_centroid(bolts)

    for bolt in bolts:
        user_x = bolt[1][0]
        user_y = bolt[1][1]
        local_x = user_x - x_cent
        local_y = user_y - y_cent
        bolt[3][0] = local_x
        bolt[3][1] = local_y

def calc_local_force_coords(bolts, force):
    """Calculate force coords with the centroid of the bolt group as origin."""
    x_cent, y_cent = calc_centroid(bolts)

    user_x = force[0][0]
    user_y = force[0][1]
    user_z = force[0][2]

    local_x = user_x - x_cent
    local_y = user_y - y_cent
    local_z = user_z

    force[3][0] = local_x
    force[3][1] = local_y
    force[3][2] = local_z

def calc_ixx(bolts):
    """Calculate the 2nd moment of area of the bolt pattern about the x-axis."""
    sum_ixx = 0.0
    for bolt in bolts:
        y = bolt[3][1]
        sum_ixx = sum_ixx + math.pow(y,2)
    return sum_ixx

def calc_iyy(bolts):
    """Calculate the 2nd moment of area of the bolt pattern about the y-axis."""
    sum_iyy = 0.0
    for bolt in bolts:
        x = bolt[3][0]
        sum_iyy = sum_iyy + math.pow(x,2)
    return sum_iyy

def calc_j(bolts):
    """Calculate the polar moment of area of bolt pattern about the z-axis."""
    ixx = calc_ixx(bolts)
    iyy = calc_iyy(bolts)
    return ixx + iyy
