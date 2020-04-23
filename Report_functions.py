from builtins import str
import time
import math
from Common import *
import os
import pdfkit
import configparser
# from utils.common import component
from pylatex import Document, Section, Subsection
from pylatex.utils import italic, bold
import pdflatex
import sys
import datetime
from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject


from pylatex import Document, Section, Subsection, Tabular, Tabularx,MultiColumn
from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex.utils import italic, NoEscape
from pdflatex import PDFLaTeX
import os
from pylatex import Document, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number
from pylatex.utils import bold

def min_pitch(d):
    min_pitch = 2.5*d
    d = str(d)
    min_pitch = str(min_pitch)

    min_pitch_eqn = Math(inline=True)
    min_pitch_eqn.append(NoEscape(r'\begin{aligned}p/g_{min}&= 2.5 ~ d&\\'))
    min_pitch_eqn.append(NoEscape(r'=&2.5*' + d + r'&=' + min_pitch + r'\end{aligned}'))
    return min_pitch_eqn

def max_pitch(t):

    max_pitch_1 = 32*min(t)
    max_pitch_2 = 300
    max_pitch = max(max_pitch_1,max_pitch_2)
    t = str(min(t))
    max_pitch = str(max_pitch)


    max_pitch_eqn = Math(inline=True)
    max_pitch_eqn.append(NoEscape(r'\begin{aligned}p/g_{max} &=\min(32~t,~300~mm)&\\'))
    max_pitch_eqn.append(NoEscape(r'&=\min(32 *~' + t+ r',~ 300 ~mm)\\&='+max_pitch+r'\end{aligned}'))
    return max_pitch_eqn

def min_edge_end(d_0,edge_type):
    if edge_type == 'a - Sheared or hand flame cut':
        factor = 1.7
    else:
        factor = 1.5
    min_edge_dist = round(factor * d_0,2)

    min_edge_dist = str(min_edge_dist)

    factor = str(factor)
    d_0 = str(d_0)

    min_end_edge_eqn = Math(inline=True)
    min_end_edge_eqn.append(NoEscape(r'\begin{aligned}e/e`_{min} &=[1.5~or~ 1.7] * d_0\\'))
    min_end_edge_eqn.append(NoEscape(r'&='+factor + r'*' + d_0+r'='+min_edge_dist+r' \end{aligned}'))
    return min_end_edge_eqn

def max_edge_end(f_y,t):

    epsilon = round(math.sqrt(250/f_y),2)
    max_edge_dist = round(12*t*epsilon,2)
    max_edge_dist = str(max_edge_dist)
    t = str(t)
    f_y = str(f_y)

    max_end_edge_eqn = Math(inline=True)
    max_end_edge_eqn.append(NoEscape(r'\begin{aligned}e/e`_{max} &= 12~ t~ \varepsilon&\\'))
    max_end_edge_eqn.append(NoEscape(r'\varepsilon &= \sqrt{\frac{250}{f_y}}\\'))
    max_end_edge_eqn.append(NoEscape(r'e/e`_{max}&=12 ~*'+ t + r'*\sqrt{\frac{250}{'+f_y+r'}}\\ &='+max_edge_dist+r'\\ \end{aligned}'))
    return max_end_edge_eqn

def bolt_shear_prov(f_ub,n_n,a_nb,gamma_mb,bolt_shear_capacity):
    f_ub = str(f_ub)
    n_n = str(n_n)
    a_nb = str(a_nb)
    gamma_mb= str(gamma_mb)
    bolt_shear_capacity=str(bolt_shear_capacity)
    bolt_shear_eqn = Math(inline=True)
    bolt_shear_eqn.append(NoEscape(r'\begin{aligned}V_{dsb} &= \frac{f_ub ~n_n~ A_{nb}}{\sqrt{3} ~\gamma_{mb}}\\'))
    bolt_shear_eqn.append(NoEscape(r'&= \frac{'+f_ub+'*'+n_n+'*'+a_nb+'}{\sqrt{3}~*~'+ gamma_mb+r'}\\'))
    bolt_shear_eqn.append(NoEscape(r'&= '+bolt_shear_capacity+r'\end{aligned}'))
    return bolt_shear_eqn

def bolt_bearing_prov(k_b,d,conn_plates_t_fu_fy,gamma_mb,bolt_bearing_capacity):
    t_fu_prev = conn_plates_t_fu_fy[0][0] * conn_plates_t_fu_fy[0][1]
    t = conn_plates_t_fu_fy[0][0]
    f_u = conn_plates_t_fu_fy[0][1]
    for i in conn_plates_t_fu_fy:
        t_fu = i[0] * i[1]
        if t_fu <= t_fu_prev:
            t = i[0]
            f_u = i[1]
    k_b = str(k_b)
    d = str(d)
    t = str(t)
    f_u= str(f_u)
    gamma_mb=str(gamma_mb)
    bolt_bearing_capacity = str(bolt_bearing_capacity)
    bolt_bearing_eqn = Math(inline=True)
    bolt_bearing_eqn.append(NoEscape(r'\begin{aligned}V_{dpb} &= \frac{2.5~ k_b~ d~ t~ f_u}{\gamma_{mb}}\\'))
    bolt_bearing_eqn.append(NoEscape(r'&= \frac{2.5~*'+ k_b+'*'+ d+'*'+t+'*'+f_u+'}{'+gamma_mb+r'}\\'))
    bolt_bearing_eqn.append(NoEscape(r'&='+bolt_bearing_capacity+r'\end{aligned}'))

    return bolt_bearing_eqn


def bolt_capacity_prov(bolt_shear_capacity,bolt_bearing_capacity,bolt_capacity):
    bolt_shear_capacity = str(bolt_shear_capacity)
    bolt_bearing_capacity = str(bolt_bearing_capacity)
    bolt_capacity = str(bolt_capacity)
    bolt_capacity_eqn = Math(inline=True)
    bolt_capacity_eqn.append(NoEscape(r'\begin{aligned}V_{db} &= min~ (V_{dsb}, V_{dpb})\\'))
    bolt_capacity_eqn.append(NoEscape(r'&= min~ ('+bolt_shear_capacity+','+ bolt_bearing_capacity+r')\\'))
    bolt_capacity_eqn.append(NoEscape(r'&='+ bolt_capacity+r'\end{aligned}'))

    return bolt_capacity_eqn


def HSFG_bolt_capacity_prov(mu_f,n_e,K_h,fub,Anb,gamma_mf,capacity):
    mu_f = str(mu_f)
    n_e = str(n_e)
    K_h = str(K_h)
    fub = str(fub)
    Anb = str(Anb)
    gamma_mf = str(gamma_mf)
    capacity = str(capacity)

    HSFG_bolt_capacity_eqn = Math(inline=True)
    HSFG_bolt_capacity_eqn.append(NoEscape(r'\begin{aligned}V_{dsf} & = \frac{\mu_f~ n_e~  K_h~ F_o}{\gamma_{mf}}\\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'& Where, F_o = 0.7 * f_{ub} A_{nb}\\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'V_{dsf} & = \frac{'+ mu_f + '*' + n_e + '*' + K_h +'* 0.7 *' +fub+'*'+Anb +r'}{'+gamma_mf+r'}\\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'& ='+capacity+r'\end{aligned}'))

    return HSFG_bolt_capacity_eqn

def get_trial_bolts(V_u, A_u,bolt_capacity,multiple=1):
    res_force = math.sqrt(V_u**2+ A_u**2)
    trial_bolts = multiple * math.ceil(res_force/bolt_capacity)
    V_u=str(V_u)
    A_u=str(A_u)
    bolt_capacity=str(bolt_capacity)
    trial_bolts=str(trial_bolts)
    trial_bolts_eqn = Math(inline=True)
    trial_bolts_eqn.append(NoEscape(r'\begin{aligned}R_{u} &= \sqrt{V_u^2+A_u^2}\\'))
    trial_bolts_eqn.append(NoEscape(r'n_{trial} &= R_u/ V_{bolt}\\'))
    trial_bolts_eqn.append(NoEscape(r'R_{u} &= \frac{\sqrt{'+V_u+r'^2+'+A_u+r'^2}}{'+bolt_capacity+ r'}\\'))
    trial_bolts_eqn.append(NoEscape(r'&='+trial_bolts+ r'\end{aligned}'))
    return trial_bolts_eqn



def min_plate_ht_req(beam_depth,min_plate_ht):
    beam_depth = str(beam_depth)
    min_plate_ht = str(min_plate_ht)
    min_plate_ht_eqn = Math(inline=True)
    min_plate_ht_eqn.append(NoEscape(r'\begin{aligned}0.6 * d_b&= 0.6 * '+ beam_depth + r'='+min_plate_ht+r'\end{aligned}'))
    return min_plate_ht_eqn

def min_flange_plate_ht_req(beam_width,min_flange_plate_ht):## when only outside plate is considered
    beam_width = str(beam_width)
    min_flange_plate_ht = str(min_flange_plate_ht)
    min_flange_plate_ht_eqn = Math(inline=True)
    min_flange_plate_ht_eqn.append(NoEscape(r'\begin{aligned}min~flange~plate~ht &= beam~width\\'))
    min_flange_plate_ht_eqn.append(NoEscape(r'&='+min_flange_plate_ht+r'\end{aligned}'))

    return min_flange_plate_ht_eqn

def min_inner_flange_plate_ht_req(beam_width, web_thickness,root_radius,min_inner_flange_plate_ht): ## when inside and outside plate is considered #todo
    beam_width = str(beam_width) ### same function used for max height
    min_inner_flange_plate_ht = str(min_inner_flange_plate_ht)
    web_thickness=str(web_thickness)
    root_radius=str(root_radius)
    min_inner_flange_plate_ht_eqn = Math(inline=True)
    min_inner_flange_plate_ht_eqn.append(NoEscape(r'\begin{aligned}&= \frac{B -t- (2*R1)}{2}\\'))
    min_inner_flange_plate_ht_eqn.append(NoEscape(r'&=\frac{'+beam_width+ r' -' +web_thickness+ r' - 2*'+ root_radius+r'}{2}\\'))
    min_inner_flange_plate_ht_eqn.append(NoEscape(r'&='+min_inner_flange_plate_ht+r'\end{aligned}'))

    return min_inner_flange_plate_ht_eqn


def max_plate_ht_req(connectivity,beam_depth, beam_f_t, beam_r_r, notch, max_plate_h):
    beam_depth = str(beam_depth)
    beam_f_t = str(beam_f_t)
    beam_r_r = str(beam_r_r)
    max_plate_h = str(max_plate_h)
    max_plate_ht_eqn = Math(inline=True)
    if connectivity in VALUES_CONN_1:
        max_plate_ht_eqn.append(NoEscape(r'\begin{aligned} &d_b - 2 (t_{bf} + r_{b1} + gap)\\'))
        max_plate_ht_eqn.append(NoEscape(r'&='+beam_depth+ '- 2* (' + beam_f_t + '+' + beam_r_r +r'+ 10)\\'))
    else:
        max_plate_ht_eqn.append(NoEscape(r'\begin{aligned} &d_b - t_{bf} + r_{b1} - notch_h\\'))
        max_plate_ht_eqn.append(NoEscape(r'&=' + beam_depth + '-' + beam_f_t + '+' + beam_r_r + '-'+ notch+ r'\\'))
    max_plate_ht_eqn.append(NoEscape(r'&=' + max_plate_h + '\end{aligned}'))
    return max_plate_ht_eqn

def min_plate_length_req(min_pitch, min_end_dist,bolt_line,min_length):
    min_pitch = str(min_pitch)
    min_end_dist = str(min_end_dist)
    bolt_line = str(bolt_line)
    min_length = str(min_length)
    min_plate_length_eqn = Math(inline=True)
    min_plate_length_eqn.append(NoEscape(r'\begin{aligned} &2*e_{min} + (n~c-1) * p_{min})\\'))
    min_plate_length_eqn.append(NoEscape(r'&=2*' + min_end_dist + '+(' + bolt_line + '-1) * ' + min_pitch + r'\\'))
    min_plate_length_eqn.append(NoEscape(r'&=' + min_length + '\end{aligned}'))
    return min_plate_length_eqn

def min_flange_plate_length_req(min_pitch, min_end_dist,bolt_line,min_length,gap):
    min_pitch = str( min_pitch)
    min_end_dist = str(min_end_dist)
    bolt_line = str(bolt_line)
    min_length = str(min_length)
    gap = str(gap)
    min_flange_plate_length_eqn = Math(inline=True)
    min_flange_plate_length_eqn.append(NoEscape(r'\begin{aligned} & 2[2*e_{min} + ({\frac{bolt~lines}{2}}-1) * p_{min})]\\'))
    min_flange_plate_length_eqn.append(NoEscape(r'& +\frac{gap}{2}]\\'))
    min_flange_plate_length_eqn.append(NoEscape(r'&=2*[(2*' + min_end_dist +r' + (\frac{'+bolt_line+r'}{2}' + r'-1) * ' + min_pitch + r'\\'))
    min_flange_plate_length_eqn.append(NoEscape(r'&= + \frac{'+gap+r'}{2}]\\'))

    min_flange_plate_length_eqn.append(NoEscape(r'&=' + min_length + '\end{aligned}'))
    return min_flange_plate_length_eqn

def min_plate_thk_req(t_w):
    t_w = str(t_w)
    min_plate_thk_eqn = Math(inline=True)
    min_plate_thk_eqn.append(NoEscape(r'\begin{aligned} t_w='+t_w+'\end{aligned}'))
    return min_plate_thk_eqn

def shear_yield_prov(h,t, f_y, gamma, V_dg):
    h = str(h)
    t = str(t)
    f_y = str(f_y)
    gamma = str(gamma)
    V_dg = str(V_dg)
    shear_yield_eqn = Math(inline=True)
    shear_yield_eqn.append(NoEscape(r'\begin{aligned} V_{dg} &= \frac{A_v*f_y}{\sqrt{3}*\gamma_{mo}}\\'))
    shear_yield_eqn.append(NoEscape(r'&=\frac{'+h+'*'+t+'*'+f_y+'}{\sqrt{3}*'+gamma+r'}\\'))
    shear_yield_eqn.append(NoEscape(r'&=' + V_dg + '\end{aligned}'))
    return shear_yield_eqn

def shear_rupture_prov(h, t, n_r, d_o, fu,v_dn,multiple =1):
    h = str(h)
    t = str(t)
    n_r = str(n_r)
    d_o = str(d_o)
    f_u = str(fu)
    v_dn = str(v_dn)
    multiple = str(multiple)
    shear_rup_eqn = Math(inline=True)
    shear_rup_eqn.append(NoEscape(r'\begin{aligned} V_{dn} &= \frac{0.75*A_{vn}*f_u}{\sqrt{3}*\gamma_{mo}}\\'))
    shear_rup_eqn.append(NoEscape(r'&='+multiple+ r'*('+h+'-('+n_r+'*'+d_o+'))*'+t+'*'+f_u+r'\\'))
    shear_rup_eqn.append(NoEscape(r'&=' + v_dn + '\end{aligned}'))
    return shear_rup_eqn

def shear_capacity_prov(V_dy, V_dn, V_db):
    V_d = min(V_dy,V_dn,V_db)
    V_d = str(V_d)
    V_dy = str(V_dy)
    V_dn = str(V_dn)
    V_db = str(V_db)
    shear_capacity_eqn = Math(inline=True)
    shear_capacity_eqn.append(NoEscape(r'\begin{aligned} V_d &= Min(V_{dy},V_{dn},V_{db})\\'))
    shear_capacity_eqn.append(NoEscape(r'&= Min('+V_dy+','+V_dn+','+V_db+r')\\'))
    shear_capacity_eqn.append(NoEscape(r'&='+V_d + '\end{aligned}'))
    return shear_capacity_eqn

def tension_yield_prov(l,t, f_y, gamma, T_dg):
    l = str(l)
    t = str(t)
    f_y = str(f_y)
    gamma = str(gamma)
    T_dg = str(T_dg)
    tension_yield_eqn = Math(inline=True)
    tension_yield_eqn.append(NoEscape(r'\begin{aligned} T_{dg} &= \frac{A_g*f_y}{\gamma_{mo}}\\'))
    tension_yield_eqn.append(NoEscape(r'&=\frac{'+l+'*'+t+'*'+f_y+'}{'+gamma+r'}\\'))
    tension_yield_eqn.append(NoEscape(r'&=' + T_dg + '\end{aligned}'))
    return tension_yield_eqn

def tension_rupture_prov(w_p, t_p, n_c, d_o, fu,gamma_m1,T_dn):
    w_p = str(w_p)
    t_p = str(t_p)
    n_c = str(n_c)
    d_o = str(d_o)
    f_u = str(fu)
    T_dn = str(T_dn)
    gamma_m1 = str(gamma_m1)
    Tensile_rup_eqn = Math(inline=True)
    Tensile_rup_eqn.append(NoEscape(r'\begin{aligned} T_{dn} &= \frac{0.9*A_{n}*f_u}{\gamma_{m1}}\\'))
    Tensile_rup_eqn.append(NoEscape(r'&=\frac{0.9*('+w_p+'-'+n_c+'*'+d_o+')*'+t_p+'*'+f_u+r'}{'+gamma_m1+r'}\\'))
    Tensile_rup_eqn.append(NoEscape(r'&=' + T_dn + '\end{aligned}'))
    return Tensile_rup_eqn

def tensile_capacity_prov(T_dg, T_dn, T_db):
    T_d = min(T_dg,T_dn,T_db)
    T_d = str(T_d)
    T_dg = str(T_dg)
    T_dn = str(T_dn)
    T_db = str(T_db)
    shear_capacity_eqn = Math(inline=True)
    shear_capacity_eqn.append(NoEscape(r'\begin{aligned} T_d &= Min(T_{dg},T_{dn},T_{db})\\'))
    shear_capacity_eqn.append(NoEscape(r'&= Min('+T_dg+','+T_dn+','+T_db+r')\\'))
    shear_capacity_eqn.append(NoEscape(r'&='+T_d + '\end{aligned}'))
    return shear_capacity_eqn

def mom_axial_IR_prov(M,M_d,N,N_d,IR):
    M = str(M)
    M_d = str(M_d)
    N = str(N)
    N_d = str(N_d)
    IR = str(IR)
    mom_axial_IR_eqn = Math(inline=True)
    mom_axial_IR_eqn.append(NoEscape(r'\begin{aligned} \frac{'+M+'}{'+M_d+r'}+\frac{'+N+'}{'+N_d+'}='+IR+r'\end{aligned}'))
    return mom_axial_IR_eqn
def IR_req(IR):
    IR = str(IR)
    IR_req_eqn = Math(inline=True)
    IR_req_eqn.append(NoEscape(r'\begin{aligned} \leq'+IR+'\end{aligned}'))
    return IR_req_eqn

def min_weld_size_req(conn_plates_weld,min_weld_size):
    t1 = str(conn_plates_weld[0])
    t2 = str(conn_plates_weld[0])
    tmax = str(max(conn_plates_weld))
    weld_min = str(min_weld_size)

    min_weld_size_eqn = Math(inline=True)
    min_weld_size_eqn.append(NoEscape(r'\begin{aligned} Thickness~of~Thicker~part&\\'))
    min_weld_size_eqn.append(NoEscape(r'=Max('+t1+','+t2+r')&='+tmax+r'\\'))
    min_weld_size_eqn.append(NoEscape(r'IS800:2007~cl.10.5.2.3~Table 21,&\\ t_{w_{min}} &=' + weld_min + r'\end{aligned}'))
    return min_weld_size_eqn

def max_weld_size_req(conn_plates_weld,max_weld_size):
    t1 = str(conn_plates_weld[0])
    t2 = str(conn_plates_weld[0])
    t_min = str(min(conn_plates_weld))
    weld_max = str(max_weld_size)

    max_weld_size_eqn = Math(inline=True)
    max_weld_size_eqn.append(NoEscape(r'\begin{aligned} Thickness~of~Thinner~part&\\'))
    max_weld_size_eqn.append(NoEscape(r'=Min('+t1+','+t2+r')&='+t_min+r'\\'))
    max_weld_size_eqn.append(NoEscape(r't_{w_{max}} &=' + weld_max + r'\end{aligned}'))
    return max_weld_size_eqn


def weld_strength_req(V,A,M,Ip_w,y_max,x_max,l_w,R_w):
    T_wh = str(round(M * y_max/Ip_w,2))
    T_wv = str(round(M * x_max/Ip_w,2))
    V_wv = str(round(V /l_w,2))
    A_wh = str(round(A/l_w,2))

    V = str(V)
    A = str(A)
    M = str(M)
    Ip_w = str(Ip_w)
    y_max = str(y_max)
    x_max = str(x_max)
    l_w = str(l_w)
    R_w = str(R_w)
    weld_stress_eqn = Math(inline=True)
    weld_stress_eqn.append(NoEscape(r'\begin{aligned} R_w&=\sqrt{(T_{wh}+A_{wh})^2 + (T_{wv}+V_{wv})^2}\\'))
    weld_stress_eqn.append(NoEscape(r'T_{wh}&=\frac{M*y_{max}}{I{pw}}=\frac{'+M+'*'+y_max+'}{'+Ip_w+r'}\\'))
    weld_stress_eqn.append(NoEscape(r'T_{wv}&=\frac{M*x_{max}}{I{pw}}=\frac{'+M+'*'+x_max+'}{'+Ip_w+r'}\\'))
    weld_stress_eqn.append(NoEscape(r'V_{wv}&=\frac{V}{l_w}=\frac{'+V+'}{'+l_w+r'}\\'))
    weld_stress_eqn.append(NoEscape(r'A_{wh}&=\frac{A}{l_w}=\frac{'+A+'}{'+l_w+r'}\\'))
    weld_stress_eqn.append(NoEscape(r'R_w&=\sqrt{('+T_wh+'+'+A_wh+r')^2 + ('+T_wv+'+'+V_wv+r')^2}\\'))
    weld_stress_eqn.append(NoEscape(r'&='+R_w+r'\end{aligned}'))

    return weld_stress_eqn

def weld_strength_prov(conn_plates_weld_fu,gamma_mw,t_t,f_w):

    f_u = str(min(conn_plates_weld_fu))
    t_t = str(t_t)
    gamma_mw = str(gamma_mw)
    f_w = str(f_w)
    weld_strength_eqn = Math(inline=True)
    weld_strength_eqn.append(NoEscape(r'\begin{aligned} f_w &=\frac{t_t*f_u}{\sqrt{3}*\gamma_{mw}}\\'))
    weld_strength_eqn.append(NoEscape(r'&=\frac{'+t_t+'*'+f_u+'}{\sqrt{3}}*'+ gamma_mw+r'\\'))
    weld_strength_eqn.append(NoEscape(r'&='+f_w+r'\end{aligned}'))

    return weld_strength_eqn


def get_pass_fail(required, provided,relation='greater'):
    required = float(required)
    provided = float(provided)
    if provided==0:
        return 'N/A'
    else:
        if relation == 'greater':
            if required >= provided:
                return 'Pass'
            else:
                return 'Fail'
        elif relation == 'geq':
            if required >= provided:
                return 'Pass'
            else:
                return 'Fail'
        elif relation == 'leq':
            if required <= provided:
                return 'Pass'
            else:
                return 'Fail'
        else:
            if required <= provided:
                return 'Pass'
            else:
                return 'Fail'


    # doc.generate_pdf('report_functions', clean_tex=False)


# geometry_options = {"top": "2in", "bottom": "1in", "left": "0.6in", "right": "0.6in", "headsep": "0.8in"}
# doc = Document(geometry_options=geometry_options, indent=False)
# report_bolt_shear_check(doc)