# milestone_issue_checker

## 用途
- zenhubでburndown chartかけるけど、見積もり(zenhubのestimate)と実稼働時間の比較がめんどい、、という個人的な問題を解決するスクリプト
- スクリプトに指定したmilestone.titleに紐づくすべてのissueを取得して、各種情報をcsvとして出力します。
- issue上に「作業時間: {hour: float}h」とコメントしておくと作業時間として認識します。
 

## 起動に必要な設定
- config.yaml.templateからconfig.yamlを作成する
- config.yamlの以下の項目を埋める


```
target_organization: 組織名
target_repositories: 対象リポジトリのリスト
github_token: githubのアクセストークン
zenhub_token: zenhubのアクセストークン
```

アクセストークンの取得方法は、以下のサイトとかを参考にしてください。

[zenhub](https://qiita.com/i35_267/items/918bd10078bb0f162bb1)

[github](https://qiita.com/kz800/items/497ec70bff3e555dacd0)


## usage

```

main.py [-h] [-m MILESTONE]

check github/zenhub milestone

optional arguments:
  -h, --help            show this help message and exit
  -m MILESTONE, --milestone MILESTONE

```

