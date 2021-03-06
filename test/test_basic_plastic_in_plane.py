import demand
import unittest
import pdb
import math

class TestDemandPlasticInPlane(unittest.TestCase):

    def setUp(self):
        self.bolts1 = [[1,(0.0, 0.0), 1.0, [None, None], [None, None], 
                       [None, None], [None, None], None, None, None,
                       [None, None]],
                       [2,(0.0, 3.0), 1.0, [None, None], [None, None], 
                       [None, None], [None, None], None, None, None,
                       [None, None]],
                       [3,(0.0, 6.0), 1.0, [None, None], [None, None], 
                       [None, None], [None, None], None, None, None,
                       [None, None]]]
        self.force1 = [(4.0, 0.0, 0.0), (0.0, -1.0, 0.0), [None, None, None],
                        [None, None, None], None, [None, None], None]

        self.bolts2 = [[1,(0.0, 0.0), 1.0, [None, None], [None, None], 
                       [None, None], [None, None], None, None, None,
                       [None, None]],
                       [2,(0.0, 3.0), 1.0, [None, None], [None, None], 
                       [None, None], [None, None], None, None, None,
                       [None, None]],
                       [3,(0.0, 6.0), 1.0, [None, None], [None, None], 
                       [None, None], [None, None], None, None, None,
                       [None, None]],
                       [4,(6.0, 0.0), 1.0, [None, None], [None, None], 
                       [None, None], [None, None], None, None, None,
                       [None, None]],
                       [5,(6.0, 3.0), 1.0, [None, None], [None, None], 
                       [None, None], [None, None], None, None, None,
                       [None, None]],
                       [6,(6.0, 6.0), 1.0, [None, None], [None, None], 
                       [None, None], [None, None], None, None, None,
                       [None, None]]]
        self.force2 = [(23.0, 8.0, 0.0), (0.6, -0.8, 0.0), [None, None, None],
                        [None, None, None], None, [None, None], None]

    def tearDown(self):
        del self.bolts1
        del self.force1
        del self.bolts2
        del self.force2

    def test_calc_instanteous_center_1(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts1)
        demand.calc_force_coords_wrt_centroid(self.bolts1, self.force1)
        demand.calc_moments_about_centroid(self.force1)

        cx_ic = -1.5
        cy_ic = 0.0

        px = self.force1[1][0]
        py = self.force1[1][1]
        mo = self.force1[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts1, px, py, mo, x0,
                                                    y0)

        self.assertAlmostEqual(cx_ic, x_ic, places=3)
        self.assertAlmostEqual(cy_ic, y_ic, places=3)


    def test_calc_instanteous_center_2(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts2)
        demand.calc_force_coords_wrt_centroid(self.bolts2, self.force2)
        demand.calc_moments_about_centroid(self.force2)

        cx_ic = -0.632 
        cy_ic = -0.474 

        px = self.force2[1][0]
        py = self.force2[1][1]
        mo = self.force2[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts2, px, py, mo, x0,
                                                    y0)

        self.assertAlmostEqual(cx_ic, x_ic, places=3)
        self.assertAlmostEqual(cy_ic, y_ic, places=3)

    def test_calc_bolt_location_wrt_ic_1(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts1)
        demand.calc_force_coords_wrt_centroid(self.bolts1, self.force1)
        demand.calc_moments_about_centroid(self.force1)
        px = self.force1[1][0]
        py = self.force1[1][1]
        mo = self.force1[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts1, px, py, mo, x0,
                                                    y0)

        demand.calc_bolt_location_wrt_ic(self.bolts1, x_ic, y_ic)

        cd  = [3.354, 1.5, 3.354]

        for bolt, d in zip(self.bolts1, cd):
            self.assertAlmostEqual(bolt[7], d, places=3)

    def test_calc_bolt_location_wrt_ic_2(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts2)
        demand.calc_force_coords_wrt_centroid(self.bolts2, self.force2)
        demand.calc_moments_about_centroid(self.force2)
        px = self.force2[1][0]
        py = self.force2[1][1]
        mo = self.force2[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts2, px, py, mo, x0,
                                                    y0)

        demand.calc_bolt_location_wrt_ic(self.bolts2, x_ic, y_ic)

        cd  = [3.463,2.415,4.204,4.424,3.662,5.025]

        for bolt, d in zip(self.bolts2, cd):
            self.assertAlmostEqual(bolt[7], d, places=3)

    def test_calc_mp_1(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts1)
        demand.calc_force_coords_wrt_centroid(self.bolts1, self.force1)
        demand.calc_moments_about_centroid(self.force1)
        px = self.force1[1][0]
        py = self.force1[1][1]
        mo = self.force1[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts1, px, py, mo, x0,
                                                    y0)
        delta_angle = demand.calc_delta_angle(px, py)

        demand.calc_force_location_wrt_ic(self.force1, x_ic, y_ic, delta_angle)

        mp = demand.calc_mp(self.force1)

        c_mp = -5.5

        self.assertAlmostEqual(mp, c_mp, places=3)

    def test_calc_mp_2(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts2)
        demand.calc_force_coords_wrt_centroid(self.bolts2, self.force2)
        demand.calc_moments_about_centroid(self.force2)
        px = self.force2[1][0]
        py = self.force2[1][1]
        mo = self.force2[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts2, px, py, mo, x0,
                                                    y0)
        delta_angle = demand.calc_delta_angle(px, py)

        demand.calc_force_location_wrt_ic(self.force2, x_ic, y_ic, delta_angle)

        mp = demand.calc_mp(self.force2)

        c_mp = -19.789

        self.assertAlmostEqual(mp, c_mp, places=3)

    def test_calc_moment_about_ic_1(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts1)
        demand.calc_force_coords_wrt_centroid(self.bolts1, self.force1)
        demand.calc_moments_about_centroid(self.force1)
        px = self.force1[1][0]
        py = self.force1[1][1]
        mo = self.force1[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts1, px, py, mo, x0,
                                                    y0)
        demand.calc_bolt_location_wrt_ic(self.bolts1, x_ic, y_ic)

        c_sum_m = 7.894
        deltas = [0.340, 0.1521, 0.340] 
        rs = [0.9815, 0.8731, 0.9815]

        sum_m = demand.calc_moment_about_ic(self.bolts1)

        self.assertAlmostEqual(c_sum_m, sum_m, places=3)
        
        for bolt, c_delta, c_r in zip(self.bolts1, deltas, rs):
            delta = bolt[8]
            r = bolt[9]
            self.assertAlmostEqual(c_delta, delta, places=3)
            self.assertAlmostEqual(c_r, r, places=3)

    def test_calc_moment_about_ic_2(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts2)
        demand.calc_force_coords_wrt_centroid(self.bolts2, self.force2)
        demand.calc_moments_about_centroid(self.force2)
        px = self.force2[1][0]
        py = self.force2[1][1]
        mo = self.force2[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts2, px, py, mo, x0,
                                                    y0)
        demand.calc_bolt_location_wrt_ic(self.bolts2, x_ic, y_ic)

        c_sum_m = 22.210 #example gives 22.207
        deltas = [0.234, 0.163, 0.284, 0.299, 0.248, 0.340] 
        rs = [0.9458, 0.8870, 0.9674, 0.9720, 0.9530, 0.9815]

        sum_m = demand.calc_moment_about_ic(self.bolts2)

        self.assertAlmostEqual(c_sum_m, sum_m, places=3)
        
        for bolt, c_delta, c_r in zip(self.bolts2, deltas, rs):
            delta = bolt[8]
            r = bolt[9]
            self.assertAlmostEqual(c_delta, delta, places=3)
            self.assertAlmostEqual(c_r, r, places=3)

    def test_calc_force_location_wrt_ic_1(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts1)
        demand.calc_force_coords_wrt_centroid(self.bolts1, self.force1)
        demand.calc_moments_about_centroid(self.force1)
        px = self.force1[1][0]
        py = self.force1[1][1]
        mo = self.force1[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts1, px, py, mo, x0,
                                                    y0)
        delta_angle = demand.calc_delta_angle(px, py)

        c_df_x = 5.500
        c_df_y = -3.000
        
        demand.calc_force_location_wrt_ic(self.force1, x_ic, y_ic, delta_angle)

        df_x = self.force1[5][0]
        df_y = self.force1[5][1]

        self.assertAlmostEqual(c_df_x, df_x, places=3)
        self.assertAlmostEqual(c_df_y, df_y, places=3)


    def test_calc_force_location_wrt_ic_2(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts2)
        demand.calc_force_coords_wrt_centroid(self.bolts2, self.force2)
        demand.calc_moments_about_centroid(self.force2)
        px = self.force2[1][0]
        py = self.force2[1][1]
        mo = self.force2[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts2, px, py, mo, x0,
                                                    y0)
        delta_angle = demand.calc_delta_angle(px, py)

        c_df_x = 20.632
        c_df_y = 5.474
        
        demand.calc_force_location_wrt_ic(self.force2, x_ic, y_ic, delta_angle)

        df_x = self.force2[5][0]
        df_y = self.force2[5][1]

        self.assertAlmostEqual(c_df_x, df_x, places=3)
        self.assertAlmostEqual(c_df_y, df_y, places=3)


    def test_calc_r_1(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts1)
        demand.calc_force_coords_wrt_centroid(self.bolts1, self.force1)
        demand.calc_moments_about_centroid(self.force1)
        px = self.force1[1][0]
        py = self.force1[1][1]
        mo = self.force1[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts1, px, py, mo, x0,
                                                    y0)
        delta_angle = demand.calc_delta_angle(px, py)

        c_r = 5.500

        demand.calc_r(self.force1, x_ic, y_ic, delta_angle)

        r = self.force1[6]

        self.assertAlmostEqual(c_r, r, places=3)

    
    def test_calc_r_2(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts2)
        demand.calc_force_coords_wrt_centroid(self.bolts2, self.force2)
        demand.calc_moments_about_centroid(self.force2)
        px = self.force2[1][0]
        py = self.force2[1][1]
        mo = self.force2[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts2, px, py, mo, x0,
                                                    y0)
        delta_angle = demand.calc_delta_angle(px, py)

        c_r = 19.789

        demand.calc_r(self.force2, x_ic, y_ic, delta_angle)

        r = self.force2[6]
        
        self.assertAlmostEqual(c_r, r, places=3)


    def test_calc_force_location_wrt_ic(self):
        pass


    def test_calc_plastic_reactions_1(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts1)
        demand.calc_force_coords_wrt_centroid(self.bolts1, self.force1)
        demand.calc_moments_about_centroid(self.force1)
        px = self.force1[1][0]
        py = self.force1[1][1]
        mo = self.force1[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts1, px, py, mo, x0,
                                                    y0)
        delta_angle = demand.calc_delta_angle(px, py)

        demand.calc_force_location_wrt_ic(self.force1, x_ic, y_ic, delta_angle)

        mp = demand.calc_mp(self.force1)

        demand.calc_bolt_location_wrt_ic(self.bolts1, x_ic, y_ic)

        c_sum_rux = 0.0000
        c_sum_ruy = 1.220
        c_sum_m = 7.894

        sum_rux, sum_ruy, sum_m = demand.calc_bolt_fraction_reactions(self.bolts1, mp)

        self.assertAlmostEqual(c_sum_rux, sum_rux, places=3)
        self.assertAlmostEqual(c_sum_ruy, sum_ruy, places=3)
        self.assertAlmostEqual(c_sum_m, sum_m, places=3)

    def test_calc_plastic_reactions_2(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts2)
        demand.calc_force_coords_wrt_centroid(self.bolts2, self.force2)
        demand.calc_moments_about_centroid(self.force2)
        px = self.force2[1][0]
        py = self.force2[1][1]
        mo = self.force2[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts2, px, py, mo, x0,
                                                    y0)
        delta_angle = demand.calc_delta_angle(px, py)

        demand.calc_force_location_wrt_ic(self.force2, x_ic, y_ic, delta_angle)

        mp = demand.calc_mp(self.force2)

        demand.calc_bolt_location_wrt_ic(self.bolts2, x_ic, y_ic)

        c_sum_rux = -0.472
        c_sum_ruy = 0.347
        c_sum_m = 22.210

        sum_rux, sum_ruy, sum_m = demand.calc_bolt_fraction_reactions(self.bolts2, mp)

        self.assertAlmostEqual(c_sum_rux, sum_rux, places=3)
        self.assertAlmostEqual(c_sum_ruy, sum_ruy, places=3)
        self.assertAlmostEqual(c_sum_m, sum_m, places=3)

    def test_iterate_to_ic_1(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts1)
        demand.calc_force_coords_wrt_centroid(self.bolts1, self.force1)
        demand.calc_moments_about_centroid(self.force1)
        px = self.force1[1][0]
        py = self.force1[1][1]
        mo = self.force1[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts1, px, py, mo, x0,
                                                    y0)
        delta_angle = demand.calc_delta_angle(px, py)

        demand.calc_force_location_wrt_ic(self.force1, x_ic, y_ic, delta_angle)

        demand.calc_bolt_location_wrt_ic(self.bolts1, x_ic, y_ic)
        
        mp = demand.calc_mp(self.force1)

        c_x2 = -0.9907
        c_y2 = 0.0000

        x2, y2, ce, cu = demand.iterate_to_ic(self.bolts1, self.force1)

        self.assertAlmostEqual(c_x2, x2, places=3)
        self.assertAlmostEqual(c_y2, y2, places=3)

        
    def test_iterate_to_ic_2(self):
        demand.calc_bolt_coords_wrt_centroid(self.bolts2)
        demand.calc_force_coords_wrt_centroid(self.bolts2, self.force2)
        demand.calc_moments_about_centroid(self.force2)
        px = self.force2[1][0]
        py = self.force2[1][1]
        mo = self.force2[2][2]
        x0 = 0.0
        y0 = 0.0
        x_ic, y_ic = demand.calc_instanteous_center(self.bolts2, px, py, mo, x0,
                                                    y0)
        delta_angle = demand.calc_delta_angle(px, py)

        demand.calc_force_location_wrt_ic(self.force2, x_ic, y_ic, delta_angle)

        mp = demand.calc_mp(self.force2)

        demand.calc_bolt_location_wrt_ic(self.bolts2, x_ic, y_ic)

        c_x2 = -1.2967
        c_y2 = -0.5835


        x2, y2, ce, cu = demand.iterate_to_ic(self.bolts2, self.force2)

        self.assertAlmostEqual(c_x2, x2, places=3)
        self.assertAlmostEqual(c_y2, y2, places=3)
