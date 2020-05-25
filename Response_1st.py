### 参考：https://qiita.com/hanon/items/d5afd8ea3f1e2e7b0d32
from control.matlab import *
import numpy as np
from ipywidgets import interact
from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure, output_file
from bokeh.layouts import row, column

output_notebook() # jupyterNotebookに出力

### 描画
## 初期データ

#制御対象
K  = 1
T  = 0.5
G1 = tf( [K], [T, 1] )

K  = 1
z  = 0.7
wn = 10
G2 = tf( [K*wn**2], [1, 2*z*wn, wn**2] )

G = G1
y,t = step(G, np.arange(0, 5, 0.01))

gain, _, w = bode(G, logspace(-2, 2), Plot=False)

## figureを宣言
p1 = figure(title = "Step Response",
          plot_height = 250,
          plot_width = 350,
          y_range=(0,2),
          x_axis_label='t [s]',
          y_axis_label='y')

## figureを宣言
p2 = figure(title = "Pole",
          plot_height = 250,
          plot_width = 250,
          x_range = (-18, 2),
          y_range = (-10, 10),
          x_axis_label='Re',
          y_axis_label='Im')

## figureを宣言
p3 = figure(title = "Gain Diagram",
          plot_height = 250,
          plot_width = 600,
          x_axis_type = 'log',
          y_range = (-60, 20),
          x_axis_label='w [rad/s]',
          y_axis_label='Gain [dB]')

## rendererを追加
p1.line(t, 1*(t>0))
r1 = p1.line(t, y, line_width = 3, color='red')
pole = G.pole()
r2 = p2.scatter(pole.real, pole.imag)
gain, _, w = bode(G, logspace(-2,2), Plot=False)
r3 = p3.line(w, 20*np.log10(gain), line_width = 3)


## interactorを定義
def update(K=1, T=1):
    G = tf( [K], [T, 1] )
    yout,_ = step(G, np.arange(0, 5, 0.01))
    r1.data_source.data['y'] = yout
    pole = G.pole();
    r2.data_source.data['x'] = pole.real
    r2.data_source.data['y'] = pole.imag
    gain, _, _ = bode(G, logspace(-2,2), Plot=False)
    r3.data_source.data['y'] = 20*np.log10(gain)
    push_notebook()

## 描画
p0 = row(p1,p2)
p = column(p0, p3)
show(p, notebook_handle=True) # notebook_handleをTrueにすると後から図を制御出来る

## interactorの実行
interact(update, K = (0.1, 2, 0.1), T = (-0.1, 2, 0.05) )