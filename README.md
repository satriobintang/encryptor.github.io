
# Dokumentasi Final Project Pemrograman Python dan Pemrograman Web

### Deskripsi singkat final project
Kriptografi merupakan salah satu hal penting yang dibutuhkan ketika masuk ke dunia
cyber security. Dengan adanya kriptografi, maka ketika kita mengirim sebuah pesan rahasia
tidak perlu khawatir bisa dibaca oleh orang lain yang disebut dengan enkripsi pesan,
sebaliknya para hacker professional selalu menggunakan kriptografi ketika menemukan
pesan berbahaya yang tidak bisa dibaca oleh orang lain yaitu dengan cara mendekripsikan
pesan tersebut sehingga bisa dibaca. Oleh karena itu, project akhir kami juga akan membuat
pesan kriptografi enkripsi dan dekripsi dengan berbagai macam algoritma unik.

### library/package  
Adapun library yang kami gunakan pada final project ini, yaitu Base64 yang merupakan Python Standard Library. 
Base 64 adalah teknik menerjemahkan data biner yang berbentuk ASCII. Kegunaan dari teknik ini adalah
untuk menyembunyikan data penting. Jadi teknik encoding dan decoding ini bertujuan
sebagai cryptography.

### Progres ide final project
Dari target yang diinginkan, progress final project ini sudah mencapai 95%, karena dari
sekian banyak algoritma yang kelompok kami buat hanya beberapa saja yang bisa kami
implemetasikan ke dalam web.

### Nama Anggota Kelompok
1. Andi Muhammad Ichsan Jalaluddin (20.83.0545)
2. Rangga Wahyu Setiawan (20.83.0548)
3. Satrio Bintang Pamungkas (20.83.0552)

<br/>
<br/>

# Flask-Encryptor

A Flask extension based on `simple-crypt-using-flask-and-python` which allows simple and secure encryption and decryption for Python.

## Overview

This Flask extension provides two functions, which encrypt and decrypt data, delegating all the hard work to the [encryptor](https://github.com/satriobintang/encryptor.github.io).

## Dependencies

 - Flask 2.0.1 or greater

## Requirements and installation

In order to work, encryptor project is based on these following modules:

- Flask

To install Flask, simply:

```bash
> pip install Flask
```

## Installation
you can download the repository and install manually by running:

```bash
> set FLASK_APP=server.py
> set FLASK_ENV=development
> flask run
```

## Steps To Run 

- Clone or download the repository
- Have [Python](https://www.python.org/downloads/) installed on your machine
- Download [Flask](http://flask.pocoo.org/)
- Start a local Flask web server
  - In a terminal or command prompt, navigate to the downloaded folder and run `python server.py`. (The flask docs have an alternate way of doing this.) 
  - In a browser, go to the URL indicated by `Running on http://XXX.X.X.X:YYYY/` 
- Enjoy

## Algorithms

The algorithm used to implement this project is:

* Base 32

* Base 64

* Caesar Cipher

* Shared Key Secret

* RSA

## Credits

Most of the work has been completed thanks to [Alt5chm3rz](https://github.com/satriobintang), Andi, and Rangga. Focus of this project is to 'develop' it.

>Special thanks to @Bachittarjeet for encouraging

>I hope this project can be useful for many people. -Alt5chm3rz
