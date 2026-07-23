import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from gestion_utilisateurs import ajouter_utilisateur, authentifier_utilisateur, lister_utilisateurs
import os

class Application(tk.Tk):
    def __init__(self):
        # Initialiser la base de données si besoin
        try:
            from database import initialiser_bdd
            initialiser_bdd()
        except Exception as e:
            print(f"Erreur initialisation BDD: {e}")
        super().__init__()
        self.title("Système de gestion financière")
        self.geometry("400x300")
        self.configurer_style_treeview()
        self.creer_interface_connexion()

    def configurer_style_treeview(self):
        style = ttk.Style()
        style.configure("Treeview",
                       background="white",
                       foreground="black",
                       rowheight=25)
        style.map("Treeview",
                 background=[("selected", "black")],
                 foreground=[("selected", "white")])

    def creer_interface_connexion(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Connexion", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Email").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()
        tk.Label(self, text="Mot de passe").pack()
        self.mdp_entry = tk.Entry(self, show="*")
        self.mdp_entry.pack()
        tk.Button(self, text="Se connecter", command=self.connexion).pack(pady=10)
        tk.Button(self, text="Créer un compte", command=self.creer_interface_inscription).pack()

    def creer_interface_inscription(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Inscription", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Nom").pack()
        self.nom_entry = tk.Entry(self)
        self.nom_entry.pack()
        tk.Label(self, text="Email").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()
        tk.Label(self, text="Mot de passe").pack()
        self.mdp_entry = tk.Entry(self, show="*")
        self.mdp_entry.pack()
        tk.Button(self, text="S'inscrire", command=self.inscription).pack(pady=10)
        tk.Button(self, text="Retour", command=self.creer_interface_connexion).pack()

    def connexion(self):
        email = self.email_entry.get()
        mdp = self.mdp_entry.get()
        utilisateur = authentifier_utilisateur(email, mdp)
        if utilisateur:
            self.creer_interface_principale(utilisateur)
        else:
            messagebox.showerror("Erreur", "Identifiants invalides")

    def inscription(self):
        nom = self.nom_entry.get()
        email = self.email_entry.get()
        mdp = self.mdp_entry.get()
        if ajouter_utilisateur(nom, email, mdp):
            messagebox.showinfo("Succès", "Compte créé !")
            self.creer_interface_connexion()
        else:
            messagebox.showerror("Erreur", "Email déjà utilisé")

    def creer_interface_principale(self, utilisateur):
        # Après authentification, ouvrir l'ancienne interface principale (main.py) dans une nouvelle fenêtre
        import subprocess
        import sys
        self.destroy()  # Fermer la fenêtre de connexion
        # Calculer le chemin absolu de main.py dans le même projet
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        main_path = os.path.join(base_dir, 'main.py')
        # Lancer le bon main.py (celui du projet courant) avec le cwd correct
        subprocess.Popen([sys.executable, main_path], cwd=base_dir)

    def afficher_utilisateurs_tableau(self):
        from tkinter import ttk
        utilisateurs = lister_utilisateurs()
        win = tk.Toplevel(self)
        win.title("Liste des utilisateurs")
        win.geometry("500x300")
        win.configure(bg="#f5f6fa")
        columns = ("Nom", "Email", "Rôle")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        for u in utilisateurs:
            tree.insert("", "end", values=(u[1], u[2], u[4] if len(u) > 4 else "utilisateur"))
        tree.pack(expand=True, fill="both", padx=10, pady=10)
        ttk.Button(win, text="Fermer", command=win.destroy).pack(pady=5)

    def generer_rapport_ventes(self):
        from rapports import generer_rapport_ventes_pdf
        generer_rapport_ventes_pdf()
        messagebox.showinfo("Rapport PDF", "Rapport des ventes généré : rapport_ventes.pdf")

    def generer_rapport_clients(self):
        from rapports import generer_rapport_clients_pdf
        generer_rapport_clients_pdf()
        messagebox.showinfo("Rapport PDF", "Rapport des clients généré : rapport_clients.pdf")

    def generer_rapport_produits(self):
        from rapports import generer_rapport_produits_pdf
        generer_rapport_produits_pdf()
        messagebox.showinfo("Rapport PDF", "Rapport des produits généré : rapport_produits.pdf")

    def afficher_utilisateurs(self):
        utilisateurs = lister_utilisateurs()
        users_str = "\n".join([f"{u[1]} ({u[2]}) - {u[3]}" for u in utilisateurs])
        messagebox.showinfo("Utilisateurs", users_str)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
