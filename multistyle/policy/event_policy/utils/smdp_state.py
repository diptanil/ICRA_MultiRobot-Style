class SeqMDPState:
    def __init__(self, em, sa, va):
        self.em_state = em
        self.sa_state = sa
        self.va_state = va

        self.str_name = "(" + str(em) + ", " + str(sa) + ", " + str(va) + ")"

    def __str__(self):
        return self.str_name

    def is_equal(self, st):
        if self.em_state == st.em_state and self.sa_state == st.sa_state and self.va_state == st.va_state:
            return True
        else:
            return False


class SeqMDPAction:
    def __init__(self, act_seq_dn):

        self.self_action = act_seq_dn[-1]
        self.act_seq_dn = act_seq_dn

    def __str__(self):
        return str(self.act_seq_dn)
