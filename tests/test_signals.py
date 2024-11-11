from django.test import TestCase
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from book.models import Patient, User
from book.signals import createPatient, updateUser


class SignalTests(TestCase):

    def setUp(self):
        # Déconnecter les signaux pendant les tests
        post_save.disconnect(createPatient, sender=User)
        post_save.disconnect(updateUser, sender=Patient)

    def tearDown(self):
        # Reconnecter les signaux après les tests
        post_save.connect(createPatient, sender=User)
        post_save.connect(updateUser, sender=Patient)

    def test_create_patient_signal(self):
        # Créer un utilisateur avec le rôle de patient
        user = User.objects.create_user(email='patient@example.com', password='password123', is_patient=True)

        # Reconnecter le signal et simuler le post_save
        post_save.connect(createPatient, sender=User)
        createPatient(User, instance=user, created=True)

        # Vérifier que le patient a été créé
        self.assertTrue(Patient.objects.filter(user=user).exists())
        patient = Patient.objects.get(user=user)
        self.assertTrue(patient.serial_number.startswith('#PT'))

    def test_update_user_signal(self):
        # Créer un utilisateur avec le rôle de patient
        user = User.objects.create_user(email='patient@example.com', password='password123', is_patient=True)
        patient = Patient.objects.create(user=user, serial_number='test123', first_name='John', last_name='Doe')

        # Reconnecter le signal et simuler le post_save
        post_save.connect(updateUser, sender=Patient)
        patient.first_name = 'Jane'
        patient.save()

        # Vérifier que l'utilisateur a été mis à jour
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Jane')


if __name__ == "__main__":
    TestCase.main()