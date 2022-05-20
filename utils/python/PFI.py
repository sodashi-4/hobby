import sys
import warnings
from dataclasses import dataclass
from typing import Any
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib


from sklearn.metrics import mean_squared_error

@dataclass
class PermutationFeatureImportance:
  """Permutation Feature Importance (PFI)

  Args:
      estimator: 学習済みモデル
      X: 特徴量
      y: 目的変数
      var_names: 特徴量の名前
  """

  estimator: Any
  X: np.ndarray
  y: np.ndarray
  var_names:list[str]


  def __post_init__(self) -> None:
    #シャッフルなしの場合の予測精度
    #mean_squared_error()はsquared=TrueならMSE, squared=FalseならRMSE
    self.baseline = mean_squared_error(
      self.y, self.estimator.predict(self.X), squared=False
    )

  
  def _permutation_metrics(self, idx_to_permute: int) -> float:
    """ある特徴量の値をシャッフルしたときの予測精度を求める
    
    Args:
        idx_to_permute: シャッフルする特徴量のインデックス
    """

    #シャッフルする際に、元の特徴量が上書きされないようにコピー
    X_permuted = self.X.copy()

    #特徴量の値をシャッフルして予測
    X_permuted[:, idx_to_permute] = np.random.permutation(
      X_permuted[:, idx_to_permute]
    )
    y_pred = self.estimator.predict(X_permuted)
    return mean_squared_error(self.y, y_pred, squared=False)

  
  def permutation_feature_importance(self, n_shuffle:int = 10) -> None:
    """PFIを求める
    
    Args:
        n_shuffle: シャッフルの回数。多いほど値が安定する。デフォルトは１０回
    """

    J = self.X.shape[1] #特徴量の数

    #J個の特徴量に対してPFIを求めたい
    #R回シャッフルを繰り返して平均を取ることで値を安定させている
    metrics_permuted = [
      np.mean(
        [self._permutation_metrics(j) for r in range(n_shuffle)]
        )
        for j in range(J)
    ]

    #データフレームとしてまとめる
    # シャッフルでどのくらい予測精度が落ちるかは、
    #差と比率の２種類を用意する
    df_feature_importance = pd.DataFrame(
      data = {
        "var_name" : self.var_names,
        "baseline" : self.baseline,
        "permutation" : metrics_permuted,
        "difference" : metrics_permuted - self.baseline,
        "ratio" : metrics_permuted / self.baseline
      }
    )
    self.feature_importance = df_feature_importance.sort_values(
      "permutation", ascending=False
    )

  def plot(self, importance_type : str = "difference") ->None:
    """PFIを可視化
    
    Args:
        importance_type: PFIを差と比率どちらで計算するか
    """

    fig, ax = plt.subplots()
    ax.barh(
      self.feature_importance["var_name"],
      self.feature_importance[importance_type],
      label = f"baseline: {self.baseline:.2f}",
    )
    ax.set(xlabel=importance_type, ylabel=None)
    ax.invert_yaxis()
    ax.legend(loc="lower right")
    fig.suptitle(f"Permutationによる特徴量の重要度({importance_type})")

    fig.show()