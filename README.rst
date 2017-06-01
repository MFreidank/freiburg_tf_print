==================
Freiburg_TF_Print
==================


Overview
========

This tool provides means to remotely print any document at the computer pool of 
the Albert-Ludwigs University in Freiburg. 

It is essentially a lightweight wrapper around LPD (`Line Printer Daemon
<https://en.wikipedia.org/wiki/Berkeley_printing_system>`_) 
and uses SSH with your pool account credentials at the university for 
authentification. 

You can either specify your printer of choice or have the 
tool find the fastest available choice for you automatically.

We also provide facilities to: 
    * print only certain pages from a document 
    * provide feedback on the cost of your print job (only for PDF documents) 
