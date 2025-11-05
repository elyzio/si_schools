from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.http import JsonResponse
from estudante.models import Estudante, EstudanteUser, EstudanteClasse, EstudanteEncarregadu, EstudanteDokumentu, EstudanteTransfer
from estudante.forms import EstudanteForm, EstudanteClasseForm, EstudanteEncarregaduForm, EstudanteDokumentuForm, EstudanteTransferForm
from custom.models import Ano
from datetime import datetime