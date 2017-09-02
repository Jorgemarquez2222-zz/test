from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.files.storage import get_storage_class
from django.contrib.staticfiles.templatetags.staticfiles import static
from app_public.app.tools import *
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.utils import translation
from app_public.app.tools import log_error
import os

from app_public.forms.appointment_creation_form import AppointmentCreationForm
from app_public.models import *
from app_public.forms import *
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from app_public.forms import LocationForm


# email;fn;ln;pwd/
data_fake_users = "Tena.Manis@mail.com;Tena;Manis;azerty42/Alisha.Dunkerson@mail.com;Alisha;Dunkerson;azerty42/Virginia.Hanline@mail.com;Virginia;Hanline;azerty42/Raeann.Reddix@mail.com;Raeann;Reddix;azerty42/Ettie.Mccallum@mail.com;Ettie;Mccallum;azerty42/Catina.Healey@mail.com;Catina;Healey;azerty42/Thalia.Bast@mail.com;Thalia;Bast;azerty42/Hoyt.Hackbarth@mail.com;Hoyt;Hackbarth;azerty42/Mel.Mazer@mail.com;Mel;Mazer;azerty42/Gilma.Grissett@mail.com;Gilma;Grissett;azerty42/Audra.Krupa@mail.com;Audra;Krupa;azerty42/Shayne.Wetherby@mail.com;Shayne;Wetherby;azerty42/Tomoko.Tutor@mail.com;Tomoko;Tutor;azerty42/Peggy.Roosevelt@mail.com;Peggy;Roosevelt;azerty42/Bea.Cowden@mail.com;Bea;Cowden;azerty42/Manda.Rooker@mail.com;Manda;Rooker;azerty42/Candyce.Seeber@mail.com;Candyce;Seeber;azerty42/Edwina.Suddeth@mail.com;Edwina;Suddeth;azerty42/Natacha.Fellers@mail.com;Natacha;Fellers;azerty42/Wilton.Lard@mail.com;Wilton;Lard;azerty42/Monika.Delgadillo@mail.com;Monika;Delgadillo;azerty42/Kristy.Cupps@mail.com;Kristy;Cupps;azerty42/Leonie.Doggett@mail.com;Leonie;Doggett;azerty42/Grisel.Cote@mail.com;Grisel;Cote;azerty42/Latoyia.Felker@mail.com;Latoyia;Felker;azerty42/Jamee.Conaway@mail.com;Jamee;Conaway;azerty42/Numbers.Samuelson@mail.com;Numbers;Samuelson;azerty42/Anitra.Socha@mail.com;Anitra;Socha;azerty42/Lakeshia.Dell@mail.com;Lakeshia;Dell;azerty42/Clarissa.Kisner@mail.com;Clarissa;Kisner;azerty42/Bernice.Haar@mail.com;Bernice;Haar;azerty42/Tobias.Mulloy@mail.com;Tobias;Mulloy;azerty42/Francesco.Garret@mail.com;Francesco;Garret;azerty42/Jone.Nolin@mail.com;Jone;Nolin;azerty42/Cecilia.Grothe@mail.com;Cecilia;Grothe;azerty42/Tomas.Atkin@mail.com;Tomas;Atkin;azerty42/Richard.Golay@mail.com;Richard;Golay;azerty42/Lisa.Kleeman@mail.com;Lisa;Kleeman;azerty42/Vernell.Bachelder@mail.com;Vernell;Bachelder;azerty42/Kimbery.Navarette@mail.com;Kimbery;Navarette;azerty42/Preston.Carbonaro@mail.com;Preston;Carbonaro;azerty42/Tona.Lariviere@mail.com;Tona;Lariviere;azerty42/Margherita.Whetzel@mail.com;Margherita;Whetzel;azerty42/Lizette.Remley@mail.com;Lizette;Remley;azerty42/Kraig.Maas@mail.com;Kraig;Maas;azerty42/Shaunte.Buitron@mail.com;Shaunte;Buitron;azerty42/Alberto.Bice@mail.com;Alberto;Bice;azerty42/Avery.Glisson@mail.com;Avery;Glisson;azerty42/Diane;Smale.Zora@mail.com;Diane;Smale/Jenniffer.Sizemore@mail.com;Jenniffer;Sizemore;azerty42/Yasmin.Tapscott@mail.com;Yasmin;Tapscott;azerty42/Annetta.Learned@mail.com;Annetta;Learned;azerty42/April.Tunney@mail.com;April;Tunney;azerty42/Bart.Kumm@mail.com;Bart;Kumm;azerty42/Danny.Branstetter@mail.com;Danny;Branstetter;azerty42/Romelia.Mericle@mail.com;Romelia;Mericle;azerty42/Ozie.Farris@mail.com;Ozie;Farris;azerty42/Dovie.Yeatman@mail.com;Dovie;Yeatman;azerty42/Clementina.Noss@mail.com;Clementina;Noss;azerty42/Ester.Morrone@mail.com;Ester;Morrone;azerty42/Mariana.Garrick@mail.com;Mariana;Garrick;azerty42/Anitra.Elizondo@mail.com;Anitra;Elizondo;azerty42/Melonie.Songer@mail.com;Melonie;Songer;azerty42/Herminia.Sandstrom@mail.com;Herminia;Sandstrom;azerty42/Calvin.Peake@mail.com;Calvin;Peake;azerty42/Matilde.Arnold@mail.com;Matilde;Arnold;azerty42/Chang.Hedges@mail.com;Chang;Hedges;azerty42/Sung.Denner@mail.com;Sung;Denner;azerty42/Denyse.Relyea@mail.com;Denyse;Relyea;azerty42/Shaneka.Kupiec@mail.com;Shaneka;Kupiec;azerty42/Aron.Mee@mail.com;Aron;Mee;azerty42/Burt.Veltri@mail.com;Burt;Veltri;azerty42/Darci.Ellers@mail.com;Darci;Ellers;azerty42/Shemeka.Nottingham@mail.com;Shemeka;Nottingham;azerty42/Elia.Ranger@mail.com;Elia;Ranger;azerty42/Myrna.Hawes@mail.com;Myrna;Hawes;azerty42/Crystle.Mattei@mail.com;Crystle;Mattei;azerty42/Larue.Coury@mail.com;Larue;Coury;azerty42/Shirlene.Potvin@mail.com;Shirlene;Potvin;azerty42/Sybil.Ake@mail.com;Sybil;Ake;azerty42/Virginia.Kallas@mail.com;Virginia;Kallas;azerty42/Herta.Seim@mail.com;Herta;Seim;azerty42/Evangeline.Atwell@mail.com;Evangeline;Atwell;azerty42/Jacinta.Rosebrock@mail.com;Jacinta;Rosebrock;azerty42/Darlena.Gosselin@mail.com;Darlena;Gosselin;azerty42/Toni.Alred@mail.com;Toni;Alred;azerty42/Dion.Cutshaw@mail.com;Dion;Cutshaw;azerty42/Edison.Delaune@mail.com;Edison;Delaune;azerty42/Milly.Hamada@mail.com;Milly;Hamada;azerty42/Augusta.Bryden@mail.com;Augusta;Bryden;azerty42/Shena.Mork@mail.com;Shena;Mork;azerty42/Nanette.Trenholm@mail.com;Nanette;Trenholm;azerty42/Warner.Payton@mail.com;Warner;Payton;azerty42/Ouida.Souza@mail.com;Ouida;Souza;azerty42/Lauralee.Mcalexander@mail.com;Lauralee;Mcalexander;azerty42/Laraine.Heap@mail.com;Laraine;Heap;azerty42/Vanna.Willard@mail.com;Vanna;Willard;azerty42/Fabian.Shrout@mail.com;Fabian;Shrout;azerty42/Jonah.Quandt@mail.com;Jonah;Quandt;azerty42/Hannelore.Schewe@mail.com;Hannelore;Schewe;azerty42/Tara.Cale@mail.com;Tara;Cale;azerty42/Kymberly.Nau@mail.com;Kymberly;Nau;azerty42/Kittie.Pellegrino@mail.com;Kittie;Pellegrino;azerty42/Mellisa.Jelinek@mail.com;Mellisa;Jelinek;azerty42/Cassey.Maciel@mail.com;Cassey;Maciel;azerty42/Shawnee.Boyett@mail.com;Shawnee;Boyett;azerty42/Brenna.Krauth@mail.com;Brenna;Krauth;azerty42/Bryant.Golder@mail.com;Bryant;Golder;azerty42/Voncile.Broyles@mail.com;Voncile;Broyles;azerty42/Analisa.Garnett@mail.com;Analisa;Garnett;azerty42/Isiah.Eagan@mail.com;Isiah;Eagan;azerty42/Mallie.Villafana@mail.com;Mallie;Villafana;azerty42/Adeline.Beatrice@mail.com;Adeline;Beatrice;azerty42/Yuki.Carbo@mail.com;Yuki;Carbo;azerty42/Oscar.Speth@mail.com;Oscar;Speth;azerty42/Eustolia.Hammes@mail.com;Eustolia;Hammes;azerty42/Harriet.Gregoire@mail.com;Harriet;Gregoire;azerty42/Nichole.Hardt@mail.com;Nichole;Hardt;azerty42/Burton.Bello@mail.com;Burton;Bello;azerty42/Margie.Weishaar@mail.com;Margie;Weishaar;azerty42/Jacinto.Crays@mail.com;Jacinto;Crays;azerty42/Lashunda.Frazee@mail.com;Lashunda;Frazee;azerty42/Elinore.Gamble@mail.com;Elinore;Gamble;azerty42/Margot.Loan@mail.com;Margot;Loan;azerty42/Emelina.Salinas@mail.com;Emelina;Salinas;azerty42/Johnsie.Rubin@mail.com;Johnsie;Rubin;azerty42/Sasha.Verrill@mail.com;Sasha;Verrill;azerty42/Charlene.Castellano@mail.com;Charlene;Castellano;azerty42/Sofia.Kurek@mail.com;Sofia;Kurek;azerty42/Miss.Burchell@mail.com;Miss;Burchell;azerty42/Earnest.Dawson@mail.com;Earnest;Dawson;azerty42/Pansy.Pal@mail.com;Pansy;Pal;azerty42/Jann.Vanlandingham@mail.com;Jann;Vanlandingham;azerty42/Melonie.Cali@mail.com;Melonie;Cali;azerty42/Raeann.Chia@mail.com;Raeann;Chia;azerty42/Rachelle.Coyle@mail.com;Rachelle;Coyle;azerty42/Abel.Pollitt@mail.com;Abel;Pollitt;azerty42/Marva.Popejoy@mail.com;Marva;Popejoy;azerty42/Iris.Sturgill@mail.com;Iris;Sturgill;azerty42/Eugenio.Ellerbe@mail.com;Eugenio;Ellerbe;azerty42/Majorie.Ungar@mail.com;Majorie;Ungar;azerty42/Harmony.Strauch@mail.com;Harmony;Strauch;azerty42/Dotty.Shell@mail.com;Dotty;Shell;azerty42/Neta.Stow@mail.com;Neta;Stow;azerty42/Avis.Brink@mail.com;Avis;Brink;azerty42/Elliott.Newlon@mail.com;Elliott;Newlon;azerty42/Leandra.Horrigan@mail.com;Leandra;Horrigan;azerty42/Corliss.Randel@mail.com;Corliss;Randel;azerty42/Leoma.Auton@mail.com;Leoma;Auton;azerty42"
data_fake_groups = "Aerolíneas Federales/Alaska y los Pegamoides/Alaska y Dinarama/Amaral/Amarok/Amistades Peligrosas/Amparanoia/Andy & Lucas/Ángeles del Infierno/Antònia Font/Avalanch/Aventuras de Kirlian/Aviador Dro/Azúcar Moreno/Baccara/Barón Rojo/Barrabás/Barricada/Bellepop/Betagarri/Boikot/Bravo/Los Bravos/Los Brincos/La Buena Vida/Cadillac/Café Quijano/Los Canarios/El Canto Del Loco/La Casa Azul/Celtas Cortos/Chambao/Los Chichos/Chucho/Los Chunguitos/Cómplices/Contradanza/Danza Invisible/DarkSun/Darna/La Década Prodigiosa/Décima Víctima/Def Con Dos/Los del Mar/Los del Río/Los Diablos/Dixebra/D'Nash/Dover/Duncan Dhu/Dúo Dinámico/Dvicio/Elefantes/Los Elegantes/Ella Baila Sola/Eskorbuto/Esplendor Geométrico/Estopa/La Excepción/Extremoduro/El Último de la Fila/Facto delafé y las flores azules/Family/Fangoria/Fito y los Fitipaldis/Forever Slave/Fórmula V/Los Gandules/Golpes Bajos/Las Grecas/La Guardia/Hamlet/Héroes del Silencio/Hidrogenesse/Hinds/Hombres G/Itoiz/Jarabe de Palo/K-Narias/Ketama/The Killer Barbies/Kortatu/KUDAI/Lax'n'Busto/Le Mans/Leño/Los Limones/Lole y Manuel/Lunae/Macaco/Machetazo/Mägo de Oz/Marea/Marlango/M-Clan/Mecano/Mezquita/Milladoiro/Mocedades/Modestia Aparte/Mojinos Escozíos/La Musgaña/Los Mustang/Nacha Pop/Negu Gorriak/Nena Daconte/Los Nikis/Nosoträsh/Ñu/OBK/Obrint Pas/Obús/Ojos de Brujo/La Oreja De Van Gogh/Orquesta Mondragón/La Pandilla/Parálisis Permanente/Parchís/Pastora/Pata Negra/Los Pekenikes/Pereza/Els Pets/Pignoise/Un Pingüino en mi Ascensor/The Pinker Tones/Los Planetas/Platero y Tú/La Polla Records/Los Pop Tops/Presuntos Implicados/Los Punsetes/La Quinta Estación/Radio Futura/Reincidentes/Relative Silence/Os Resentidos/Los Rodríguez/Russian Red/Sangre Azul/Santa Justa Klan/Sau/Sauze/Savia/Sergio y Estíbaliz/Sex Museum/Sexy Sadie/Siempre Así/Siniestro Total/Los Sírex/Ska-P/Skalariak/Skizoo/Smash/Sôber/Sonblue/Sopa de Cabra/Soziedad Alkoholika/Stravaganzza/Los Suaves/El Sueño de Morfeo/Las Supremas de Móstoles/Tahúres zurdos/Tako/Tequila/Los Terribles Pedorros/Tess/Tierra Santa/Los Toreros Muertos/Triana/La Unión (Spanish)/El Último de la Fila/The Unfinished Sympathy"
data_fake_specialities = "Accident and emergency medicine/Adolescent medicine/Aerospace medicine/Allergology/Allergy and immunology/AnaesthesiologyAnaesthetics/Biological hematology/Cardiology/Cardiothoracic surgery/Child and adolescent psychiatry and psychotherapy/Childpsychiatry/Clinical biology/Clinical chemistry/Clinical neurophysiology/Colon and Rectal Surgery/Craniofacial surgery/Dental,oral and maxillo-facial surgery/Dermato-venerology/Dermatology/Dermatology-Venereology/Emergency medicine/EndocrinologyGastro-enterologic surgery/Gastroenterology/General hematology/General Practice/General practice/General surgery/GeriatricsHealth informatics/Hospice and palliative medicine/Immunology/Infectious disease/Infectious diseases/Internal medicineInterventional radiology/Laboratory medicine/Maxillo-facial surgery/Microbiology/Neonatology/Nephrology/Neuro-psychiatryNeurology/Neuroradiology/Neurosurgery/Nuclear medicine/Obstetrics and gynaecology/Obstetrics and gynecology/Occupationalmedicine/Ophthalmology/Oral and maxillofacial surgery/Orthodontics/Orthopaedics/Otorhinolaryngology/Paediatric allergologyPaediatric cardiology/Paediatric endocrinology and diabetes/Paediatric gastroenterology, hepatology and nutrition/Paediatrichaematology and oncology/Paediatric infectious diseases/Paediatric nephrology/Paediatric respiratory medicine/Paediatricrheumatology/Paediatric surgery/Paediatrics/Pathology/Pharmacology/Physical medicine and rehabilitation/Plastic surgeryPlastic, reconstructive and aesthetic surgery/Podiatric medicine/Podiatric Surgery/Psychiatry/Public Health/Public health andPreventive Medicine/Pulmonology/Radiology/Radiotherapy/Respiratory medicine/Rheumatology/Sports medicine/Stomatology/Thoracicsurgery/Tropical medicine/Urology/Vascular medicine/Vascular surgery/Venereology"
def create_user(email, first_name, last_name, pwd):
    user = User.objects.create_user(
            username=email,
            email=email,
            password=pwd,
            first_name=first_name,
            last_name=last_name)
    doctor = Doctor(user=user)
    user.save()
    doctor.save()
def create_fake_users():
    users = data_fake_users.split('/')
    for u in users:
        data = u.split(';')
        try:
            create_user(data[0], data[1], data[2], data[3])
        except Exception:
            pass
def create_fake_groups():
    groups = data_fake_groups.split('/')
    for g in groups:
        DoctorGroup(name=g).save()
def create_fake_specialities():
    specialities = data_fake_specialities.split('/')
    for s in specialities:
        Speciality(name=s).save()

@method_decorator(login_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class ViewTest(TemplateView):
    template_name = "test.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': AppointmentCreationForm()})
        if 'createfakeusers' in request.GET.keys():
            create_fake_users()
        if 'createfakegroups' in request.GET.keys():
            create_fake_groups()
        if 'createfakespecialities' in request.GET.keys():
            create_fake_specialities()
        if 'populate' in request.GET.keys():
            create_fake_users()
            create_fake_groups()
            create_fake_specialities()
        return render(request, self.template_name)
        return JsonResponse({})
        form = ProfileForm()
        return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'message': 'OKOKOKOKOK'})
        return render(request, "message_display.html", {'message': 'Hello world !','sub_message': 'This is the message...', 'sub_sub_message': 'Only the fool could ignore it.'})
        return HttpResponseBadRequest()
        myval = 0
        if 'myval' in request.COOKIES.keys():
            myval = int(request.COOKIES['myval'])
            myval += 1
        response = render(request, self.template_name, {})
        response.set_cookie('myval', myval)
        return response

    def post(self, request, *args, **kwargs):
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, self.template_name, {'form': form})
        form = ProfileForm(request.POST)
        if form.is_valid():
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form, 'error':1})
        return render(request, self.template_name, {})
        return redirect('/test')

        file = request.FILES['myfile']

        if (not check_image_extension(file.name)):
            return redirect('/')

        save_path = static('media/logo/logo.png')
        while os.path.isfile(save_path):
            save_path = static('media/foto/' + get_random_filename() + '.' + file.name.split('.')[-1])

        return JsonResponse({'data' : save_path})

        with open(save_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        return redirect('/test')
        #return JsonResponse({'data' : request.FILES['myfile']})