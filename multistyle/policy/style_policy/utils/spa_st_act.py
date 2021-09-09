class SPA_st:
    def __init__(self, jpg_st, style):

        self.jpg_st = jpg_st
        self.style = style

        self.str_name = '(' + str(jpg_st) + ',' + str(style) + ')'

    def __str__(self):
        return self.str_name

    def is_equal(self, state):
        if self.jpg_st.is_equal(state.jpg_st) and self.style == state.style:
            return True
        else:
            return False

# class SPA_act:
#
#     def __init__(self, act):
#         self.action = act