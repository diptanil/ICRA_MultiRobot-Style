class MTEG_st:
    def __init__(self, em, e, sa, v):
        self.em_st = em
        self.sa_st = sa
        self.events = e
        self.v_sts = v

        if self.events == "":
            self.str_name = "(" + str(em) + ", " + str(sa) + ", " + str(v) + ")"
        else:
            self.str_name = "(" + str(em) + str(e) + ", " + str(sa) + ", " + str(v) + ")"

    def __str__(self):
        return self.str_name

    def str_wo_evt(self):
        return "(" + str(self.em_st) + ", " + str(self.sa_st) + ", " + str(self.v_sts) + ")"

    def is_equal(self, st):
        if self.em_st == st.em_st and self.events == st.events and self.sa_st == st.sa_st and self.v_sts == st.v_sts:
            return True
        else:
            return False