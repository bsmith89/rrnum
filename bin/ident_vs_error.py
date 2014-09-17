#!/usr/bin/env python

from sys import argv
from pandas import read_table
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from numpy import array, log2, sqrt, mean, linspace
from scipy.stats import norm


def middle_half(seq):
    try:
        first_quartile = seq[int(0.25 * len(seq))]
    except IndexError:
        first_quartile = float('nan')
    try:
        second_quartile = seq[int(0.75 * len(seq))]
    except:
        second_quartile = float('nan')
    return first_quartile, second_quartile


def moving_window(exog, endog, window, func=mean):
    exog = array(exog)
    endog = array(endog)
    xs = linspace(min(exog), max(exog))
    ys = []
    for i, x in enumerate(xs):
        wind_l = max(min(exog), x - window / 2.)
        wind_h = min(max(exog), x + window / 2.)
        values = endog[(exog > wind_l) & (exog < wind_h)]
        ys.append(func(values))
    return xs, array(ys)


def main():
    inpath = argv[1]
    data = read_table(inpath)
    data['log2fold'] = (log2(data.copy1) - log2(data.copy2))
    data['sqlog2fold'] = data.log2fold ** 2

    # Calculate empirical interquartile range
    data_sorted = data.sort('log2fold')
    iq_xs, interquartile = \
        moving_window(data_sorted.perc_ident,
                      data_sorted.log2fold,
                      window=0.1, func=middle_half)
    iq_low, iq_hi = interquartile.T

    # Calculate parametric interquartile range (50% prediction interval)
    var_xs, var_estimate = moving_window(data.perc_ident,
                                         data.sqlog2fold,
                                         window=0.1)
    pred_low = norm.ppf(0.25, scale=sqrt(var_estimate))
    pred_hi = norm.ppf(0.75, scale=sqrt(var_estimate))

    # Plot everything
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    ax.fill_between(iq_xs, iq_low, iq_hi,
                    color='k', alpha=0.1, lw=0)

    ax.plot(var_xs, pred_low, '--', c='k')
    ax.plot(var_xs, pred_hi, '--', c='k')

    scat = ax.scatter(data.perc_ident, data.log2fold, c=data.copy1,
                      s=5, lw=0, alpha=0.05, norm=LogNorm())
    cb = plt.colorbar(scat)
    cb.set_alpha(1)
    cb.draw_all()
    cb.set_label("$c_1$", size=20, rotation='horizontal')
    cb.set_ticks(range(1, 15))

    ax.set_xlim((0.5, 1))
    ax.set_ylim((-4, 4))
    ax.set_xlabel("Sequence Identity", size=20)
    ax.set_ylabel("$\log_2(c_1 / c_2)$", size=20)

    plt.savefig("fig/ident_vs_error.png")

if __name__ == "__main__":
    main()
