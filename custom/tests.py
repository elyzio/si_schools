# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import (
    Distrito, Subdistrito, Suco, Aldeia,
    Ano, Departamentu, Classe, Turma, Periodo, Materia
)

class DistritoModelTest(TestCase):
    def setUp(self):
        # Create test data
        self.distrito = Distrito.objects.create(nome="Dili")
    
    def test_distrito_creation(self):
        """Test that a distrito can be created"""
        self.assertEqual(self.distrito.nome, "Dili")
    
    def test_distrito_str(self):
        """Test the string representation"""
        self.assertEqual(str(self.distrito), "Dili")
    
    def test_distrito_unique(self):
        """Test that distrito nome must be unique"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Distrito.objects.create(nome="Dili")  # Duplicate


class SubdistritoModelTest(TestCase):
    def setUp(self):
        self.distrito = Distrito.objects.create(nome="Dili")
        self.subdistrito = Subdistrito.objects.create(
            nome="Cristo Rei",
            distrito=self.distrito
        )
    
    def test_subdistrito_creation(self):
        """Test subdistrito is linked to distrito"""
        self.assertEqual(self.subdistrito.distrito, self.distrito)
    
    def test_subdistrito_str(self):
        """Test string representation"""
        self.assertEqual(str(self.subdistrito), "Cristo Rei (Dili)")
    
    def test_subdistrito_cascade_delete(self):
        """Test that deleting distrito deletes subdistrito"""
        distrito_id = self.distrito.id
        self.distrito.delete()
        self.assertFalse(Subdistrito.objects.filter(distrito_id=distrito_id).exists())


class AnoModelTest(TestCase):
    def setUp(self):
        self.ano = Ano.objects.create(ano=2024, is_active=True)
    
    def test_ano_creation(self):
        """Test ano is created correctly"""
        self.assertEqual(self.ano.ano, 2024)
        self.assertTrue(self.ano.is_active)
    
    def test_only_one_active_ano(self):
        """Test that only one ano can be active"""
        ano2 = Ano.objects.create(ano=2025, is_active=True)
        
        # Refresh from database
        self.ano.refresh_from_db()
        
        # First ano should no longer be active
        self.assertFalse(self.ano.is_active)
        self.assertTrue(ano2.is_active)
    
    def test_ano_str(self):
        """Test string representation"""
        self.assertEqual(str(self.ano), "2024")


class MateriaModelTest(TestCase):
    def setUp(self):
        self.dept = Departamentu.objects.create(
            departamento="Mathematics",
            sigla="MATH"
        )
        self.materia = Materia.objects.create(
            materia="Algebra",
            departamentu=self.dept,
            codigo="MATH101",
            descricao="Basic algebra course"
        )
    
    def test_materia_creation(self):
        """Test materia is created with all fields"""
        self.assertEqual(self.materia.materia, "Algebra")
        self.assertEqual(self.materia.codigo, "MATH101")
        self.assertEqual(self.materia.departamentu, self.dept)
    
    def test_materia_str(self):
        """Test string representation"""
        self.assertEqual(str(self.materia), "MATH101 - Algebra")
    
    def test_codigo_unique(self):
        """Test that codigo must be unique"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Materia.objects.create(
                materia="Geometry",
                codigo="MATH101"  # Duplicate code
            )