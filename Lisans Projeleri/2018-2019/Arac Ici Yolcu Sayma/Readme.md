Öncelikle model dosyalarının inmesi gerekiyor. Bulabildiğim 2 model dosyasının linkini paylaşıyorum.

1-  https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/                 ---->(prototxt ve caffemodel dosyaları inecek.)

2-  https://github.com/raunaqness/Gender-and-Age-Detection-OpenCV-Caffe

Bunları indirdikten sonra Pycharm'ı indirip yüklemek gerekiyor.

Pycharm kolay bir programdır; hem model dosyaları için dosya konumları yazmak zorunda kalmazsınız(Raspberry Pi 3 kullanılacaksa dosya konumları yazmak zorunda kalabilirsiniz.) hem de OpenCV gibi eklentileri yüklemek(File/Settings/Project İnterpreter. Oradaki + ya basıp gelen sayfadan ekleyebilirsiniz) sorun olmaz.

Gerekli Kodların py uzatısını koydum. İndirdiğiniz model dosyalarını, Yüz ve göz tanıması için xml dosyalarını kodları yazdığınız klasör içine atın(Pycharm için). Sorunsuz Çalışacaktır.
