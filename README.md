# Encryption-Code
## 使用技術 <img src="https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat">
##  本プロジェクトの目的
鍵更新型暗号の仕組みを学び、Python による実装を⾏う。実装を⾏った署名⽅式は、Abdalla-Reyzin署名・Forward-Secure署名・Key-Insulated署名の3種類である。実装した署名のプログラムは、鍵⽣成・署名⽣成・署名検証・鍵更新に分けて実⾏時間の計測を⾏い、性能の評価をする。さらに、プログラムの改善点も検討する。次に、本プロジェクトでの成果を説明する。実装では、Abdalla-Reyzin 署名・Forward-Secure署名・Key-Insulated署名を実現できた。しかし、Key-Insulated署名の鍵更新は実現することができなかった。この原因は、鍵更新に伴う安全な環境の秘密鍵の引き継ぎが実装できなったことにある。安全な環境の秘密鍵 𝑆𝐾∗をグローバル変数によってこれを解決しようとしたが、安全性が保証れないため断念した。また、各署名⽅式における素数⽣成の⽅法だが、Abdalla-Reyzin 署名・Forward-Secure 署名では、フェルマーの⼩定理、Key-Insulated署名ではミラーラビン素数判定⽅式を採⽤している。
