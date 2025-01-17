# to-do list for training `speculator`

Fill out the `done` column in the table below with the date in which the training has been completed

| done | model       | training batches | n_pca | pca training batches | 99% accuracy | dPCA plot |
| ---- | ----------- | ------- | ----- | ------------------------ | ------------ |---|
| CHH 10/20/2020     | simpledust  | 300     | 20    | 200                      |   4%           | |
| KJK 10/21/2020     | simpledust  | 300     | 20    | 200                      |   -4.0%, 4.5%           | |
|      | simpledust  | 300     | 30    | 200                      |              ||
| KJK 10/23/2020     | simpledust  | 300     | 40    | 200                      |   -4.8%, 4.6%           | |
| CHH 10/26/2020     | complexdust | 300     | 30    | 200                      |   -8.7%, 10%            | |
| KJK 10/26/2020     | complexdust | 300     | 30    | 200                      |   -4.8%, 5.5%            | [link](https://github.com/kgb0255/GQPMC_v4_JAMES/blob/9eb748d6336746b93b2024f0e33f4cd9932a6b4e/dPCA_plots/complexdust.pca_30.batch_0_299.dfrac.pdf)|
|      | complexdust | 300     | 40    | 200                      |              ||
| KJK 10/27/2020     | complexdust | 400     | 30    | 200                      |   -5.7%, 6.8%             | [link](https://github.com/kgb0255/GQPMC_v4_JAMES/blob/9eb748d6336746b93b2024f0e33f4cd9932a6b4e/dPCA_plots/complexdust.pca_30.batch_0_399.dfrac.pdf)|
| KJK 10/28/2020     | complexdust | 400     | 40    | 200                      |   -5.4%, 5.5%             | [link](https://github.com/kgb0255/GQPMC_v4_JAMES/blob/9eb748d6336746b93b2024f0e33f4cd9932a6b4e/dPCA_plots/complexdust.pca_40.batch_0_399.dfrac.pdf)|
| KJK 10/28/2020     | complexdust | 400     | 50    | 200                      |   -4.6%, 5.2%             | [link](https://github.com/kgb0255/GQPMC_v4_JAMES/blob/9eb748d6336746b93b2024f0e33f4cd9932a6b4e/dPCA_plots/complexdust.pca_50.batch_0_399.dfrac.pdf)|
| KJK 10/29/2020     | complexdust | 400     | 60    | 200                      |   -4.9%, 6.0%             | [link](https://github.com/kgb0255/GQPMC_v4_JAMES/blob/9eb748d6336746b93b2024f0e33f4cd9932a6b4e/dPCA_plots/complexdust.pca_60.batch_0_399.dfrac.pdf)|
| KJK 10/31/2020     | complexdust | 500     | 40    | 200                      |   -5.6%, 7.0%             | [link](https://github.com/kgb0255/GQPMC_v4_JAMES/blob/9eb748d6336746b93b2024f0e33f4cd9932a6b4e/dPCA_plots/complexdust.pca_40.batch_0_499.dfrac.pdf)|
| CHH 10/31/2020     | complexdust | 200     | 30, 30, 30 | 400 | -10%, 10% | |
| CHH 10/29/2020*     | complexdust | 400     | 30, 30, 30 | 400 | -10%, 6% | |
| CHH 10/29/2020*     | complexdust | 400     | 40, 40, 40 | 400 | -10%, 7.5% | |
| CHH 10/29/2020*     | complexdust | 400     | 50, 50, 50 | 400 | -10%, 8% | |
| [CHH 11/02/2020](https://github.com/changhoonhahn/gqp_mc/blob/aa20b7223c8fab5a6ccd654a7c2e7257dd245739/nb/validate_trained_desi_complexdust_speculator_wavebins.ipynb)      | complexdust | 500     | 30, 30, 30 | 500 | (-7.5%, 7%), (-1.8%, -1.8%), (<-1%, 1%) | |
| [CHH 11/03/2020](https://github.com/changhoonhahn/gqp_mc/blob/de0ebadce064876c7054bea4006a47136c49a3c5/nb/validate_trained_desi_complexdust_speculator_wavebins.ipynb)      | complexdust | 500     | 40, 40, 30 | 500 | (-8%, 7.5%), (-1.5%, -1.5%), (<-1%, 1%) | |
| [CHH 11/03/2020](https://github.com/changhoonhahn/gqp_mc/blob/acf8b79e0a7f82969e6df63604b660b2de9abf4e/nb/validate_trained_desi_complexdust_speculator_wavebins.ipynb)      | complexdust | 500     | 40, 50, 30 | 500 | (-8%, 7.5%), (-2.%, -2.%), (<-1%, 1%) | |
| [CHH 11/05/2020](https://github.com/changhoonhahn/gqp_mc/blob/3e92fdaad20e2241f634d12987daa5e159b03ce9/nb/validate_trained_desi_complexdust_speculator_wavebins.ipynb)      | complexdust | 200, 200, 500     | 30, 30, 30 | 500 | (-5%, 4%), (-1.%, 1.%), (<-1%, 1%) | |
| [CHH 11/05/2020](https://github.com/changhoonhahn/gqp_mc/blob/52b05191f5d90c9d2ce65ac96d4cba913dd97e62/nb/validate_trained_desi_complexdust_speculator_wavebins.ipynb)      | complexdust | 500 (tiger), 500 (tiger), 500     | 30, 30, 30 | 500 | worse than above | |
| [CHH 11/10/2020](https://github.com/changhoonhahn/gqp_mc/blob/aa12381641014cfc9e239ad5f0a0017e3f750ac5/nb/validate_trained_desi_complexdust_speculator_wavebins.ipynb)      | complexdust | 200 (colab, longer patience),-,-     | 30, -, - | 500 | (-3%, 3%) | |
| [CHH 11/11/2020](https://github.com/changhoonhahn/gqp_mc/blob/4a0eb4b30b43f08269dc94ba6e7b77bba9cae783/nb/validate_trained_desi_complexdust_speculator_wavebins.ipynb)      | complexdust | 500 (tiger, longer patience),-,-     | 50, -, - | 500 | (-3%, 2%) | |
|      |             |         |       |                          |              | |


*likely not finished training; divided speculator into 3 wavelength bins
