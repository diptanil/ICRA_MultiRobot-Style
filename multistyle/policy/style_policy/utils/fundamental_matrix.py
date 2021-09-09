import numpy as np

########################################################
# Function - to swap rows and column of matrix
# swap i,j rows/columns of a square matrix `m`
########################################################


def mat_swap(m, i, j):
    n = []
    s = len(m)

    if s != len(m[0]):
        raise Exception("Cannot swap non-square matrix")

    if i == j:
        # no need to swap
        return m

    for r in range(s):
        n_row = []
        tmp_row = m[r]
        if r == i:
            tmp_row = m[j]
        if r == j:
            tmp_row = m[i]
        for c in range(s):
            tmp_el = tmp_row[c]
            if c == i:
                tmp_el = tmp_row[j]
            if c == j:
                tmp_el = tmp_row[i]
            n_row.append(tmp_el)
        n.append(n_row)
    return n

########################################################
# Function - t_decompose
# decompose input matrix `m` on Q (t-by-t) and R (t-by-r) components
# `t` is the number of transient states
########################################################


def t_decompose(m, t):
    if t == 0:
        raise Exception("No transient states. At least initial state is needed.")

    q = []
    for r in range(t):
        q_row = []
        for c in range(t):
            q_row.append(m[r][c])
        q.append(q_row)
    if not q:
        raise Exception("Not a valid AMC matrix: no transient states")

    r = []
    for j in range(t):
        r_row = []
        for c in range(t, len(m[j])):
            r_row.append(m[j][c])
        r.append(r_row)
    if not r:
        raise Exception("Not a valid AMC matrix: missing absorbing states")
    return np.array(q), np.array(r)


########################################################
# Function - check_abs_t
# Check if other absorbing states exist in the MC and add it to the
# states which are deliberately being made absorbing state.
########################################################


def check_abs_t(t_mat, t_states, ab_st):
    temp = [t_states[i] for i in np.where(t_mat == 1)[0]]
    for i in temp:
        if i not in ab_st:
            ab_st.append(i)
    return ab_st


########################################################
#  Function - generate_b_matrix
# Generate the transition probability matrix for the modified transition
# matrix.
########################################################


def generate_b_matrix(t_mat, t_states, abs_states):
    m_t_states = t_states.copy()
    t_shape = t_mat.shape[0]
    abs_states = check_abs_t(t_mat, t_states, abs_states)
    # print(t_mat)
    abs_ind = [t_states.index(st) for st in abs_states]
    abs_ind.sort(reverse=True)
    modified_t_mat = np.identity(t_shape)
    # print(abs_states)
    # print(abs_ind)
    for ind, i in enumerate(modified_t_mat):
        if ind not in abs_ind:
            modified_t_mat[ind] = t_mat[ind]
    # print(modified_t_mat)
    count = t_shape - 1
    for i in abs_ind:
        modified_t_mat = mat_swap(modified_t_mat, i, count)
        temp = m_t_states[i]
        m_t_states[i] = m_t_states[count]
        m_t_states[count] = temp
        count = count - 1
    modified_t_mat = np.array(modified_t_mat)
    # print(modified_t_mat)
    # print(m_t_states)
    q_mat_size = t_shape - len(abs_states)
    # print(q_mat_size)
    q_mat, r_mat = t_decompose(modified_t_mat, q_mat_size)
    # print(q_mat)
    # print(r_mat)
    n_mat = np.linalg.inv(np.identity(q_mat_size) - q_mat)
    b_mat = np.dot(n_mat, r_mat)
    b_row = m_t_states[:q_mat_size]
    b_col = m_t_states[q_mat_size:]

    return b_mat, b_row, b_col