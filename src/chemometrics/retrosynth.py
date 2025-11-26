from rdkit import Chem
from rdkit.Chem import Draw, BRICS, AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import base64
import io

def mol_to_image_str(mol, size=(400, 200)):
    """Convert RDKit Mol to a base64 string for Streamlit."""
    try:
        img = Draw.MolToImage(mol, size=size)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except:
        return None

def decompose_drug(smiles: str):
    """
    Simulate Retrosynthesis using BRICS (fragmentation).
    Returns:
    1. Base64 Image of the Drug
    2. List of Base64 Images of the Fragments (Precursors)
    """
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return None, []
    
    # 1. Generate Image of Target
    target_img = mol_to_image_str(mol)
    
    # 2. Fragment using BRICS (Breaking Retrosynthetically Interesting Chemical Substructures)
    # This finds clean "cuts" (like breaking an amide bond)
    frags = BRICS.BreakBRICSBonds(mol)
    
    # BRICS returns a generic molecule with dummy atoms. We need to convert to fragments.
    frag_mols = Chem.GetMolFrags(frags, asMols=True)
    
    # Clean up fragments (remove dummy atoms '*')
    clean_frags = []
    for f in frag_mols:
        # Convert to SMILES and back to sanitize
        smi = Chem.MolToSmiles(f).replace('*', 'H')
        m = Chem.MolFromSmiles(smi)
        if m:
            clean_frags.append(mol_to_image_str(m, size=(200, 200)))
            
    return target_img, clean_frags
