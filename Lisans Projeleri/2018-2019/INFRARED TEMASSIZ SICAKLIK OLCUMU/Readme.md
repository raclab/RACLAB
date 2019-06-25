-Infrared Temassız Sıcaklık Ölçümü-
Bu proje ile birlikte birden fazla kızılötesi sensörlerin haberleşmesi, 
sıcaklık değerlerinin okunması ve alınan değerlerin kullanıcıya
monitörize edilmesi gerçekleşmektedir. 
Kızılötesi sensör olarak MLX90614 Kızılötesi Sıcaklık Sensörü kullanıldı.
Sensörlerin birlikte haberleşmesi için CCS C'de I2C ile haberleşme metodu kullanıldı.
Haberleşmede dikkat edilmesi gereken önemli nokta; sensör alındığında fabrikadan
0x5A adresi ile gelmektedir. Birden fazla sensörü haberleştirmek için paralel olarak
bağlamak gerektiğinden aynı adreslerde haberleşme sağlanmamaktadır. Bu yüzden
sensörlerde mutlaka adres değişikliği yapılmalıdır. Bundan dolayı driver koduna
static int Device_Address = 0x5A; kodu eklenmiştir. 
Adres değişikliği yapıldıktan sonra her sensör yeni adresleri ile birlikte
kodda tanımlanmalıdır. Projede 3 adet sensör kullanıldı ama sayısı arttırılıp,
azaltılabilir. Projede obje sıcaklığı kullanılacağından koda sadece o eklendi.
Ancak driver kodunda diğer ölçümler bulunduğundan olayı eğer istenirse ortam sıcaklığı
ölçümü de eklenebilir, kodu çağırmak yeterli olacaktır.
Ayrıca sensör yüksek hassasiyet içermektedir ve yaklaşık 8-10 cm arası sağlıklı ölçüm yapmaktadır.
Sensör değerinin °C 'a çevrilmesi de yine driver kodunun içinde mevcuttur.
Bitirme tezi dökümanlar dosyasının içerisinde mevcuttur.

