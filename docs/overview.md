Raw Data (courtesy of imdb.com)
[IMDB non-commercial licensing](https://help.imdb.com/article/imdb/general-information/can-i-use-imdb-data-in-my-software)
[IMDB dataset details](https://www.imdb.com/interfaces/)

Curated Data from source files (tab-delimited, based on a curated IMDB watchlist)
>ls -al *imdb*
-rw-r--r-- 1 User 197121  24741 Jan 19 20:28 imdb-actors-list
-rw-r--r-- 1 User 197121  11804 Jan 19 17:31 imdb-movies-list
-rw-r--r-- 1 User 197121 115389 Jan 19 20:49 name-basics-imdb.tsv
-rw-r--r-- 1 User 197121 129177 Jan 19 19:08 title-actors-imdb.tsv
-rw-r--r-- 1 User 197121 158499 Jan 19 19:46 title-basics-imdb.tsv
-rw-r--r-- 1 User 197121  21093 Jan 19 17:35 title-ratings-imdb.tsv

>wc -l *imdb*
  2469 imdb-actors-list
  1141 imdb-movies-list
  3463 name-basics-imdb.tsv
  4707 title-actors-imdb.tsv
  2566 title-basics-imdb.tsv
  1126 title-ratings-imdb.tsv
 15472 total

>head *imdb*
==> imdb-actors-list <==
nm0000137
nm0000145
nm0000157
nm0000162
nm0000176
nm0000222
nm0000227
nm0000261
nm0000268
nm0000284

==> imdb-movies-list <==
tt2256703
tt4814436
tt5066870
tt5076184
tt6185074
tt5364518
tt4648986
tt5329524
tt5340362
tt5458812

actors
==> name-basics-imdb.tsv <==
nm0000137       Bo Derek        1956    NAN
nm0000145       Sherilyn Fenn   1965    NAN
nm0000157       Linda Hamilton  1956    NAN
nm0000162       Anne Heche      1969    NAN
nm0000176       Nastassja Kinski        1961    NAN
nm0000222       Brooke Shields  1965    NAN
nm0000227       Mira Sorvino    1967    NAN
nm0000261       Karen Allen     1951    NAN
nm0000268       Ann-Margret     1941    NAN
nm0000284       Adam Baldwin    1962    NAN

roles
==> title-actors-imdb.tsv <==
tt2256703       nm0005129       actor
tt2256703       nm0358922       actress
tt2256703       nm0201437       actress
tt2256703       nm0000447       actress
tt4814436       nm0582462       actor
tt4814436       nm1032208       actress
tt4814436       nm0579728       actress
tt4814436       nm1527475       actor
tt5066870       nm1489978       actress
tt5066870       nm1148573       actor

movies
==> title-basics-imdb.tsv <==
tt2256703       tvMovie Hitched for the Holidays        2012    87      Drama,Romance
tt4814436       tvMovie A Country Wedding       2015    84      Drama,Romance
tt5066870       tvMovie Autumn Dreams   2015    84      Comedy,Drama,Romance
tt5076184       tvMovie Harvest Moon    2015    84      Action,Comedy,Drama
tt6185074       tvMovie A Cinderella Christmas  2016    93      Comedy,Romance
tt5364518       tvMovie Dater's Handbook        2016    83      Comedy,Drama,Romance
tt4648986       tvMovie A Prince for Christmas  2015    87      Comedy,Drama,Romance
tt5329524       tvMovie All Things Valentine    2016    83      Comedy,Drama,Romance
tt5340362       tvMovie Anything for Love       2016    84      Comedy,Romance
tt5458812       tvMovie Appetite for Love       2016    84      Comedy,Romance

ratings
==> title-ratings-imdb.tsv <==
tt2256703       6.6     1996
tt4814436       6.9     2742
tt5066870       6.4     3496
tt5076184       6.4     2943
tt6185074       6.3     2957
tt5364518       5.9     2166
tt4648986       6.0     1800
tt5329524       6.5     2108
tt5340362       6.5     2139
tt5458812       6.3     2072

Classes
Actor.self
Role.self
Movie.self
Rating.self

Lists
actor_list[]
role_list[]
movie_list[]
rating_list[]
