import fixpointtool.fpt_conf


class IncompatibleSetsError(Exception):
    pass


class IncompatibleFunctionsError(Exception):
    pass


class IncompatibleFunctionsForUnionError(Exception):
    pass


class NotDefinedError(Exception):
    pass


# R -> (Z -> 2^Y)  -  returns pre-image(-function) for a relation R
def pre_image(R):
    def new_f(z):
        pre_image_set = set([t[0] for t in R if t[1] == z])
        return pre_image_set
    return new_f


# Y, a -> 2^Y  -  returns potential values to reduce/increase
def potential_values(Y, a):
    if fixpointtool.fpt_conf.GFP:
        return set([y for y in Y if a(y) != fixpointtool.fpt_conf.ALGEBRA.complement(fixpointtool.fpt_conf.ALGEBRA.e)])
    else:
        return set([y for y in Y if a(y) != fixpointtool.fpt_conf.ALGEBRA.e])


# Y, a -> 2^Y  -  returns all states y where a(y) is minimal
def min_a(Y, a):
    min = fixpointtool.fpt_conf.ALGEBRA.complement(fixpointtool.fpt_conf.ALGEBRA.e)
    for y in Y:
        if a(y) < min:
            min = a(y)
    return set([y for y in Y if a(y) == min])


# Y, a -> 2^Y  -  returns all states y where a(y) is maximal
def max_a(Y, a):
    max = fixpointtool.fpt_conf.ALGEBRA.e
    for y in Y:
        if a(y) > max:
            max = a(y)
    return set([y for y in Y if a(y) == max])


# Y, p -> 2^Y  -  returns successor states (p is a distribution on Y)
def supp(Y, p):
    return set([y for y in Y if p(y) > 0])


def delta(Y, a):
    if fixpointtool.fpt_conf.GFP:
        pot_values = [y for y in Y if a(y) != fixpointtool.fpt_conf.ALGEBRA.complement(fixpointtool.fpt_conf.ALGEBRA.e)]
        distances = [fixpointtool.fpt_conf.ALGEBRA.complement(a(y)) for y in pot_values]
        return fixpointtool.fpt_conf.ALGEBRA.minimalValue(distances)
    else:
        pot_values = [y for y in Y if a(y) != fixpointtool.fpt_conf.ALGEBRA.e]
        distances = [a(y) for y in pot_values]
        return fixpointtool.fpt_conf.ALGEBRA.minimalValue(distances)


def reversed_delta(Y, a):
    if fixpointtool.fpt_conf.GFP:
        pot_values = [y for y in Y if a(y) != fixpointtool.fpt_conf.ALGEBRA.e]
        distances = [a(y) for y in pot_values]
        return fixpointtool.fpt_conf.ALGEBRA.minimalValue(distances)
    else:
        pot_values = [y for y in Y if a(y) != fixpointtool.fpt_conf.ALGEBRA.complement(fixpointtool.fpt_conf.ALGEBRA.e)]
        distances = [fixpointtool.fpt_conf.ALGEBRA.complement(a(y)) for y in pot_values]
        return fixpointtool.fpt_conf.ALGEBRA.minimalValue(distances)


def c(k, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            return k
        return new_f, set_in, set_out
    else:
        return k


def c_hash(k, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(Yin):
                return set()
            return new_new_f
        return new_f, set_in, set_out, c(k, set_in, set_out)
    else:
        def new_f(Yin):
            return set()
        return new_f


def c_iota(k, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            return delta(set_in, a)
        return new_f, set_in, set_out, c(k, set_in, set_out)
    else:
        return delta(set_in, a)


def reindexing(u, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(z):
                return a(u(z))
            return new_new_f
        return new_f, set_in, set_out
    else:
        def new_f(z):
            return a(u(z))
        return new_f


def reindexing_hash(u, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(Yin):
                res = set()
                for z in set_out:
                    if u(z) in Yin:
                        res |= {z}
                return res
            return new_new_f
        return new_f, set_in, set_out, reindexing(u, set_in, set_out)
    else:
        def new_f(Yin):
            res = set()
            for z in set_out:
                if u(z) in Yin:
                    res |= {z}
            return res
        return new_f


def reindexing_iota(u, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            return delta(set_in, a)
        return new_f, set_in, set_out, reindexing(u, set_in, set_out)
    else:
        return delta(set_in, a)


def min(R, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(z):
                minimum = fixpointtool.fpt_conf.ALGEBRA.complement(fixpointtool.fpt_conf.ALGEBRA.e)
                for y in pre_image(R)(z):
                    if fixpointtool.fpt_conf.ALGEBRA.lt(a(y), minimum):
                        minimum = a(y)
                return minimum
            return new_new_f
        return new_f, set_in, set_out
    else:
        def new_f(z):
            minimum = fixpointtool.fpt_conf.ALGEBRA.complement(fixpointtool.fpt_conf.ALGEBRA.e)
            for y in pre_image(R)(z):
                if fixpointtool.fpt_conf.ALGEBRA.lt(a(y), minimum):
                    minimum = a(y)
            return minimum
        return new_f


def min_hash(R, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(Yin):
                res = set()
                pre = pre_image(R)
                for z in potential_values(set_out, min(R, set_in, set_out, a)):
                    if fixpointtool.fpt_conf.GFP:
                        if min_a(pre(z), a).issubset(Yin):
                            res |= {z}
                    else:
                        if min_a(pre(z), a).intersection(Yin) != set():
                            res |= {z}
                return res
            return new_new_f
        return new_f, set_in, set_out, min(R, set_in, set_out)
    else:
        def new_f(Yin):
            res = set()
            pre = pre_image(R)
            for z in potential_values(set_out, min(R, set_in, set_out, a)):
                if fixpointtool.fpt_conf.GFP:
                    if min_a(pre(z), a).issubset(Yin):
                        res |= {z}
                else:
                    if min_a(pre(z), a).intersection(Yin) != set():
                        res |= {z}
            return res
        return new_f


def min_iota(R, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            if fixpointtool.fpt_conf.GFP:
                pre = pre_image(R)
                minimum = delta(set_in, a)
                for elem in potential_values(set_out, min(R, set_in, set_out, a)):
                    restricted_minima = min_a(set_in.intersection(pre(elem)), a)
                    for y in pre(elem):
                        if y not in restricted_minima:
                            for y2 in restricted_minima:
                                if fixpointtool.fpt_conf.ALGEBRA.lt(fixpointtool.fpt_conf.ALGEBRA.subtraction(a(y), a(y2)), minimum):
                                    minimum = fixpointtool.fpt_conf.ALGEBRA.subtraction(a(y), a(y2))
                                break
                return minimum
            else:
                return delta(set_in, a)
        return new_f, set_in, set_out, min(R, set_in, set_out)
    else:
        if fixpointtool.fpt_conf.GFP:
            pre = pre_image(R)
            minimum = delta(set_in, a)
            for elem in potential_values(set_out, min(R, set_in, set_out, a)):
                restricted_minima = min_a(set_in.intersection(pre(elem)), a)
                for y in pre(elem):
                    if y not in restricted_minima:
                        for y2 in restricted_minima:
                            if fixpointtool.fpt_conf.ALGEBRA.lt(fixpointtool.fpt_conf.ALGEBRA.subtraction(a(y), a(y2)), minimum):
                                minimum = fixpointtool.fpt_conf.ALGEBRA.subtraction(a(y), a(y2))
                            break
            return minimum
        else:
            return delta(set_in, a)


def max(R, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(z):
                maximum = fixpointtool.fpt_conf.ALGEBRA.e
                for y in pre_image(R)(z):
                    if fixpointtool.fpt_conf.ALGEBRA.gt(a(y), maximum):
                        maximum = a(y)
                return maximum
            return new_new_f
        return new_f, set_in, set_out
    else:
        def new_f(z):
            maximum = fixpointtool.fpt_conf.ALGEBRA.e
            for y in pre_image(R)(z):
                if fixpointtool.fpt_conf.ALGEBRA.gt(a(y), maximum):
                    maximum = a(y)
            return maximum
        return new_f


def max_hash(R, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(Yin):
                res = set()
                pre = pre_image(R)
                for z in potential_values(set_out, max(R, set_in, set_out, a)):
                    if not fixpointtool.fpt_conf.GFP:
                        if max_a(pre(z), a).issubset(Yin):
                            res |= {z}
                    else:
                        if max_a(pre(z), a).intersection(Yin) != set():
                            res |= {z}
                return res
            return new_new_f
        return new_f, set_in, set_out, max(R, set_in, set_out)
    else:
        def new_f(Yin):
            res = set()
            pre = pre_image(R)
            for z in potential_values(set_out, max(R, set_in, set_out, a)):
                if not fixpointtool.fpt_conf.GFP:
                    if max_a(pre(z), a).issubset(Yin):
                        res |= {z}
                else:
                    if max_a(pre(z), a).intersection(Yin) != set():
                        res |= {z}
            return res
        return new_f


def max_iota(R, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            if not fixpointtool.fpt_conf.GFP:
                pre = pre_image(R)
                minimum = delta(set_in, a)
                for elem in potential_values(set_out, min(R, set_in, set_out, a)):
                    restricted_maxima = max_a(set_in.intersection(pre(elem)), a)
                    for y in pre(elem):
                        if y not in restricted_maxima:
                            for y2 in restricted_maxima:
                                if fixpointtool.fpt_conf.ALGEBRA.lt(fixpointtool.fpt_conf.ALGEBRA.subtraction(a(y2), a(y)), minimum):
                                    minimum = fixpointtool.fpt_conf.ALGEBRA.subtraction(a(y2), a(y))
                                break
                return minimum
            else:
                return delta(set_in, a)
        return new_f, set_in, set_out, max(R, set_in, set_out)
    else:
        if not fixpointtool.fpt_conf.GFP:
            pre = pre_image(R)
            minimum = delta(set_in, a)
            for elem in potential_values(set_out, min(R, set_in, set_out, a)):
                restricted_maxima = max_a(set_in.intersection(pre(elem)), a)
                for y in pre(elem):
                    if y not in restricted_maxima:
                        for y2 in restricted_maxima:
                            if fixpointtool.fpt_conf.ALGEBRA.lt(fixpointtool.fpt_conf.ALGEBRA.subtraction(a(y2), a(y)),minimum):
                                minimum = fixpointtool.fpt_conf.ALGEBRA.subtraction(a(y2), a(y))
                            break
            return minimum
        else:
            return delta(set_in, a)


def add(w, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(e):
                return fixpointtool.fpt_conf.ALGEBRA.addition(a(e), w(e))
            return new_new_f
        return new_f, set_in, set_out
    else:
        def new_f(e):
            return fixpointtool.fpt_conf.ALGEBRA.addition(a(e), w(e))
        return new_f


def add_hash(w, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(Yin):
                if not fixpointtool.fpt_conf.GFP:
                    res = set([y for y in Yin if
                               fixpointtool.fpt_conf.ALGEBRA.le(w(y), fixpointtool.fpt_conf.ALGEBRA.complement(a(y)))])
                else:
                    res = potential_values(Yin, add(w, set_in, set_out, a))
                return res
            return new_new_f
        return new_f, set_in, set_out, add(w, set_in, set_out)
    else:
        def new_f(Yin):
            if not fixpointtool.fpt_conf.GFP:
                res = set([y for y in Yin if
                           fixpointtool.fpt_conf.ALGEBRA.le(w(y), fixpointtool.fpt_conf.ALGEBRA.complement(a(y)))])
            else:
                res = potential_values(Yin, add(w, set_in, set_out, a))
            return res
        return new_f


def add_iota(w, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            if not fixpointtool.fpt_conf.GFP:
                return delta(set_in, a)
            else:
                return delta(set_out, add(w, set_in, set_out, a))
        return new_f, set_in, set_out, add(w, set_in, set_out)
    else:
        if not fixpointtool.fpt_conf.GFP:
            return delta(set_in, a)
        else:
            return delta(set_out, add(w, set_in, set_out, a))


def sub(w, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(e):
                return fixpointtool.fpt_conf.ALGEBRA.subtraction(a(e), w(e))
            return new_new_f
        return new_f, set_in, set_out
    else:
        def new_f(e):
            return fixpointtool.fpt_conf.ALGEBRA.subtraction(a(e), w(e))
        return new_f


def sub_hash(w, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(Yin):
                if not fixpointtool.fpt_conf.GFP:
                    res = potential_values(Yin, sub(w, set_in, set_out, a))
                else:
                    res = set([y for y in Yin if
                               fixpointtool.fpt_conf.ALGEBRA.le(w(y), a(y))])
                return res
            return new_new_f
        return new_f, set_in, set_out, sub(w, set_in, set_out)
    else:
        def new_f(Yin):
            if not fixpointtool.fpt_conf.GFP:
                res = potential_values(Yin, sub(w, set_in, set_out, a))
            else:
                res = set([y for y in Yin if
                           fixpointtool.fpt_conf.ALGEBRA.le(w(y), a(y))])
            return res
        return new_f


def sub_iota(w, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            if not fixpointtool.fpt_conf.GFP:
                return delta(set_out, sub(w, set_in, set_out, a))
            else:
                return delta(set_in, a)
        return new_f, set_in, set_out, sub(w, set_in, set_out)
    else:
        if not fixpointtool.fpt_conf.GFP:
            return delta(set_out, sub(w, set_in, set_out, a))
        else:
            return delta(set_in, a)


def sub_z(w, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(e):
                res = a(e) - w(e)
                if res < fixpointtool.fpt_conf.ALGEBRA.e: res = fixpointtool.fpt_conf.ALGEBRA.e
                if res > fixpointtool.fpt_conf.ALGEBRA.complement(fixpointtool.fpt_conf.ALGEBRA.e): res = fixpointtool.fpt_conf.ALGEBRA.complement(fixpointtool.fpt_conf.ALGEBRA.e)
                return res
            return new_new_f
        return new_f, set_in, set_out
    else:
        def new_f(e):
            res = a(e) - w(e)
            if res < fixpointtool.fpt_conf.ALGEBRA.e: res = fixpointtool.fpt_conf.ALGEBRA.e
            if res > fixpointtool.fpt_conf.ALGEBRA.complement(
                fixpointtool.fpt_conf.ALGEBRA.e): res = fixpointtool.fpt_conf.ALGEBRA.complement(
                fixpointtool.fpt_conf.ALGEBRA.e)
            return res
        return new_f


def sub_z_hash(w, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(Yin):
                if not fixpointtool.fpt_conf.GFP:
                    res = set([y for y in Yin if
                               fixpointtool.fpt_conf.ALGEBRA.lt(0, a(y) - w(y)) and
                               fixpointtool.fpt_conf.ALGEBRA.le(a(y) - w(y), fixpointtool.fpt_conf.ALGEBRA.k)])
                else:
                    res = set([y for y in Yin if
                               fixpointtool.fpt_conf.ALGEBRA.le(0, a(y) - w(y)) and
                               fixpointtool.fpt_conf.ALGEBRA.lt(a(y) - w(y), fixpointtool.fpt_conf.ALGEBRA.k)])
                return res
            return new_new_f
        return new_f, set_in, set_out, sub_z(w, set_in, set_out)
    else:
        def new_f(Yin):
            if not fixpointtool.fpt_conf.GFP:
                res = set([y for y in Yin if
                           fixpointtool.fpt_conf.ALGEBRA.lt(0, a(y) - w(y)) and
                           fixpointtool.fpt_conf.ALGEBRA.le(a(y) - w(y), fixpointtool.fpt_conf.ALGEBRA.k)])
            else:
                res = set([y for y in Yin if
                           fixpointtool.fpt_conf.ALGEBRA.le(0, a(y) - w(y)) and
                           fixpointtool.fpt_conf.ALGEBRA.lt(a(y) - w(y), fixpointtool.fpt_conf.ALGEBRA.k)])
            return res
        return new_f


def sub_z_iota(w, set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            delta1 = delta(set_out, sub_z(w, set_in, set_out, a))
            delta2 = delta(set_in, a)
            if delta1 < delta2:
                return delta1
            else:
                return delta2
        return new_f, set_in, set_out, sub_z(w, set_in, set_out)
    else:
        delta1 = delta(set_out, sub_z(w, set_in, set_out, a))
        delta2 = delta(set_in, a)
        if delta1 < delta2:
            return delta1
        else:
            return delta2


def av(set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(p):
                sum = fixpointtool.fpt_conf.ALGEBRA.e
                for y in set_in:
                    sum += fixpointtool.fpt_conf.ALGEBRA.multi(p(y), a(y))
                return sum
            return new_new_f
        return new_f, set_in, set_out
    else:
        def new_f(p):
            sum = fixpointtool.fpt_conf.ALGEBRA.e
            for y in set_in:
                sum += fixpointtool.fpt_conf.ALGEBRA.multi(p(y), a(y))
            return sum
        return new_f


def av_hash(set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(Yin):
                res = set()
                for p in potential_values(set_out, av(set_in, set_out, a)):
                    if supp(set_in, p).issubset(Yin):
                        res |= {p}
                return res
            return new_new_f
        return new_f, set_in, set_out, av(set_in, set_out)
    else:
        def new_f(Yin):
            res = set()
            for p in potential_values(set_out, av(set_in, set_out, a)):
                if supp(set_in, p).issubset(Yin):
                    res |= {p}
            return res
        return new_f


def av_iota(set_in, set_out, a=None):
    if a is None:
        def new_f(a):
            return delta(set_in, a)
        return new_f, set_in, set_out, av(set_in, set_out)
    else:
        return delta(set_in, a)


def composition(h, g, a=None):
    if g[2] == h[1]:
        if a is None:
            def new_f(a):
                return h[0](g[0](a))
            return new_f, g[1], h[2]
        else:
            return h[0](g[0](a))
    else:
        raise IncompatibleSetsError()


def composition_hash(h, g, a=None):
    if a is None:
        def new_f(a):
            def new_new_f(Yin):
                return h[0](g[3][0](a))(g[0](a)(Yin))
            return new_new_f
        return new_f, g[1], h[2], composition(h[3], g[3])
    else:
        def new_f(Yin):
            return h[0](g[3][0](a))(g[0](a)(Yin))
        return new_f


def composition_iota(h, g, a=None):
    if a is None:
        def new_f(a):
            return fixpointtool.fpt_conf.ALGEBRA.minimalValue([g[0](a), h[0](g[3][0](a))])
        return new_f, g[1], h[2], composition(h[3], g[3])
    else:
        return fixpointtool.fpt_conf.ALGEBRA.minimalValue([g[0](a), h[0](g[3][0](a))])


def disjoint_union(*functions, a=None):
    set_in = set()
    set_out = set()
    for function in functions:
        if len(set_out & function[2]) > 0:
            raise IncompatibleFunctionsError()
        set_in |= function[1]
        set_out |= function[2]
    if a is None:
        def new_f(a):
            def new_new_f(z):
                for func in functions:
                    if z in func[2]:
                        return func[0](a)(z)
                raise NotDefinedError()
            return new_new_f
        return new_f, set_in, set_out
    else:
        def new_f(z):
            for func in functions:
                if z in func[2]:
                    return func[0](a)(z)
            raise NotDefinedError()
        return new_f


def disjoint_union_minimum(*functions, a=None):
    set_in = set()
    set_out = set()
    unifiable = len(functions) > 0
    for function in functions:
        if function[2] != functions[0][2]:
            unifiable = False
            break
    if not unifiable:
        for function in functions:
            if len(set_out & function[2]) > 0:
                raise IncompatibleFunctionsError()
            set_in |= function[1]
            set_out |= function[2]
        if a is None:
            def new_f(a):
                def new_new_f(z):
                    for func in functions:
                        if z in func[2]:
                            return func[0](a)(z)
                    raise NotDefinedError()
                return new_new_f
            return new_f, set_in, set_out
        else:
            def new_f(z):
                for func in functions:
                    if z in func[2]:
                        return func[0](a)(z)
                raise NotDefinedError()
            return new_f
    else:
        for function in functions:
            set_in |= function[1]
        set_out = functions[0][2]


def disjoint_union_maximum(*functions, a=None):
    set_in = set()
    set_out = set()
    for function in functions:
        if len(set_out & function[2]) > 0:
            raise IncompatibleFunctionsError()
        set_in |= function[1]
        set_out |= function[2]
    if a is None:
        def new_f(a):
            def new_new_f(z):
                for func in functions:
                    if z in func[2]:
                        return func[0](a)(z)
                raise NotDefinedError()
            return new_new_f
        return new_f, set_in, set_out
    else:
        def new_f(z):
            for func in functions:
                if z in func[2]:
                    return func[0](a)(z)
            raise NotDefinedError()
        return new_f


def disjoint_union_hash(*functions, a=None):
    set_in = set()
    set_out = set()
    for function in functions:
        set_in |= function[1]
        set_out |= function[2]
    if a is None:
        def new_f(a):
            def new_new_f(Yin):
                res = set()
                for func in functions:
                    def new_a(y):
                        if y in func[1]:
                            return a(y)
                        else:
                            raise NotDefinedError()
                    res |= func[0](new_a)(Yin.intersection(func[1]))
                return res
            return new_new_f
        return new_f, set_in, set_out, disjoint_union(*[func[3] for func in functions])
    else:
        def new_f(Yin):
            res = set()
            for func in functions:
                def new_a(y):
                    if y in func[1]:
                        return a(y)
                    else:
                        raise NotDefinedError()
                res |= func[0](new_a)(Yin.intersection(func[1]))
            return res
        return new_f


def disjoint_union_iota(*functions, a=None):
    set_in = set()
    set_out = set()
    for function in functions:
        set_in |= function[1]
        set_out |= function[2]
    if a is None:
        def new_f(a):
            values = []
            for func in functions:
                def new_a(y):
                    if y in func[1]:
                        return a(y)
                    else:
                        raise NotDefinedError

                values.append(func[0](new_a))
            return fixpointtool.fpt_conf.ALGEBRA.minimalValue(values)
        return new_f, set_in, set_out, disjoint_union(*[func[3] for func in functions])
    else:
        values = []
        for func in functions:
            def new_a(y):
                if y in func[1]:
                    return a(y)
                else:
                    raise NotDefinedError
            values.append(func[0](new_a))
        return fixpointtool.fpt_conf.ALGEBRA.minimalValue(values)
