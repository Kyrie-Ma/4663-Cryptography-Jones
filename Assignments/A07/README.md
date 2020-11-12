## Assignment 7 - Finding Primes

### Certification
#### 1. Shor/Pocklington
![ShorPocklington](https://user-images.githubusercontent.com/59664899/96922720-d3148a80-1475-11eb-9004-3091f4f628ba.PNG)
### Compositeness
#### 1. Fermat primality test
![Fermat](https://user-images.githubusercontent.com/59664899/96912101-6eeaca00-1467-11eb-813a-0ed94904fa54.PNG)
#### 2. Miller-Rabin and Solovay-Strassen Primality test
![Miller-Rabin](https://user-images.githubusercontent.com/59664899/96912131-7a3df580-1467-11eb-8f9d-983c6d633ea3.PNG)
#### 3. Frobenius primality test
![Frobenius](https://user-images.githubusercontent.com/59664899/96912184-8de95c00-1467-11eb-9bf0-f039b964ec63.PNG)
###### This is a variation of the Miller-Rabin test. This test is a generalization of the Lucas pseudoprime and takes about three times as long as the Miller-Rabin test to compute. However, the probability of this test returning an accurate result is about seven times better.
### Deterministic
#### 1. AKS primality test
![AKS](https://user-images.githubusercontent.com/59664899/96911973-39de7780-1467-11eb-8d15-73a67de2e39c.PNG)
##### In 2002, the first probably unconditional deterministic polynomial time test for primality was invented by Manindra Agrawal, Neeraj Kayal, and Nitin Saxena. The AKS primality test runs in Õ((log n)12) (improved to Õ((log n)7.5). in the published revision of their paper), which can be further reduced to Õ((log n)6) if the Sophie Germain conjecture is true. Subsequently, Lenstra and Pomerance presented a version of the test which runs in time Õ((log n)6) unconditionally.
#### 2.
#### Sources:
###### 1. https://en.wikipedia.org/wiki/Primality_test#Fast_deterministic_tests
