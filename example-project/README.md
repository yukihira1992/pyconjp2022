# example-project

動作確認用のプロジェクトです。

```
├── README.md
├── my_plugin                       # プラグインモジュール
│  ├── __init__.py                  # register関数を配置するプラグインモジュールのトップ
│  └── checkers                     # Checker用モジュール
│       ├── __init__.py
│       ├── nested_if_checker.py    # NestedIfCheckerの実装
│       └── print_checker.py        # PrintFunctionCheckerの実装
└── src                             # チェック対象のソースコード
    └── my_app                      # チェック対象のモジュール
        ├── __init__.py
        ├── main.py                 # エラーを含むコード
        └── print2.py               # 別名のprint関数を提供するモジュール
```

## 実装済みのルール

### PrintFunctionChecker

print関数の利用を禁止するルールです。

デフォルトは呼び出し対象の関数名をチェックするだけの実装になっています。 inferenceを利用する実装に切り替えるにはオプションに `--no-print-function-use-inference y` を指定します。

inference実装への切り替え

```sh
$ pylint --no-print-function-use-inference y src
```

### NestedIfChecker

if文のネストに上限を設定するルールです。

デフォルトでは3重のif文まで許容します。 ネストの上限値を変更するにはオプションに `--if-stmt-max-nest-level N` を指定します。

if文のネストの上限値の変更

```bash
$ pylint --if-stmt-max-nest-level 2 src
```

## Pylintのオプション

[.pylintrc](.pylintrc) でオプションを設定しています。

`disable` 及び `enable` オプションで自作のルール以外を無効化しています。 もし、このプロジェクトにルールを追加する場合は、追加したルールの `message-symbol` を `enable`
に指定するのを忘れないでください。

```
disable=all

enable=no-print-function,
       too-nested-if,
       my-new-rule,  # Add your new rule
```