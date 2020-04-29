from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

def cover_path(instance, filename):
    return "polozka/" + str(instance.id) + "/cover/" + filename


class Stat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Název státu", help_text="Vložte prosím celý název státu.",
                            unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Stát"

    def __str__(self):
        return self.name


class Zakaznik(models.Model):
    email = models.EmailField(primary_key=True)
    first_name = models.CharField(max_length=100, verbose_name="Jméno")
    last_name = models.CharField(max_length=100, verbose_name="Příjmení")
    stat = models.ForeignKey(Stat, blank=True, on_delete=models.SET(""), verbose_name="Stát")

    class Meta:
        ordering = ["last_name", "first_name", "stat"]
        verbose_name_plural = "Zákazník"

    def __str__(self):
        return f"{self.last_name}  {self.first_name}, E-mail: {self.email}"


class Zanr(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, verbose_name="Žánr")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Žánr"

    def __str__(self):
        return self.name


class Vydavatelstvi(models.Model):
    id = models.AutoField(primary_key=True)
    nazev = models.CharField(max_length=200, unique=True, verbose_name="Název")
    vznik = models.IntegerField(validators=[MinValueValidator(1800), MaxValueValidator(datetime.now().year)],
                                help_text=f"Hodnoty lze zadávat v rozmezí 1800 až {str(datetime.now().year)}.")
    sidlo = models.ForeignKey(Stat, blank=True, on_delete=models.SET(""), verbose_name="Sídlo")

    class Meta:
        ordering = ["nazev", "vznik"]
        verbose_name_plural = "Vydavatelství"

    def __str__(self):
        return f"{self.nazev}  {self.sidlo}"


class Interpret(models.Model):
    id = models.AutoField(primary_key=True)
    nazev = models.CharField(max_length=100, verbose_name="Název")

    class Meta:
        ordering = ["nazev"]
        verbose_name_plural = "Interpret"

    def __str__(self):
        return self.nazev


class Polozka(models.Model):
    id = models.AutoField(primary_key=True)
    nazev = models.CharField(max_length=100, verbose_name="Název")
    interpret = models.ManyToManyField(Interpret)
    vydavatelstvi = models.ManyToManyField(Vydavatelstvi, blank=True)
    stopaz = models.IntegerField(verbose_name="Stopáž", validators=[MinValueValidator(0)],
                                 help_text="Zadejte délku stopáže v minutách.")
    rok_vydani = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(datetime.now().year)],
                                     verbose_name="Rok vydání")

    typ = models.CharField(choices=(('ep', 'EP'),
                                    ('lp', 'LP'),
                                    ('kompilace', 'Kompilace'),
                                    ('soundtrack', 'Soundtrack'),
                                    ('singl', 'Singl'),
                                    ('remix ep', 'Remix EP')),
                           blank=True, max_length=10)
    explicitnost = models.CharField(choices=(('ano', 'Ano'), ('ne', 'Ne')), max_length=3)
    cena = models.FloatField(validators=[MinValueValidator(0)])
    zanr = models.ManyToManyField(Zanr, verbose_name="Žánr")
    cover = models.ImageField(upload_to=cover_path, verbose_name="Cover", blank=True, null=True)

    class Meta:
        ordering = ["interpret__nazev", "-rok_vydani"]
        verbose_name_plural = "Položka"

    def __str__(self):
        return f"{self.interpret.all().values('nazev')} {self.nazev}, Cena: ${self.cena}"


class Objednavka(models.Model):
    id = models.AutoField(primary_key=True)
    nazev = models.ManyToManyField(Polozka, verbose_name="Název")
    zakaznik = models.ManyToManyField(Zakaznik, verbose_name="Zákazník")

    class Meta:
        ordering = ["zakaznik__email"]
        verbose_name_plural = "Objednávka"

    def __str__(self):
        return f"{self.id} {self.zakaznik}, Polozka: {self.nazev}"
