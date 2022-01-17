function getCursorPosition(parent) {
    let selection = document.getSelection()
    let range = new Range
    range.setStart(parent, 0)
    range.setEnd(selection.anchorNode, selection.anchorOffset)
    return range.toString().length
  }
    
function setCursorPosition(ctrl,nPos){
    ctrl.focus();
    var rng=ctrl.createTextRange();
    rng.collapse();
    rng.moveStart("character",nPos);
    rng.select();
}

const KBDICT={
    'lowercase':{
        'alpha':'α','beta':'β','gamma':'γ','delta':'δ','epsilon':'ε',
        'zeta':'ζ','eta':'η','theta':'θ','iota':'ι','kappa':'κ','lambda':'λ',
        'mu':'μ','nu':'ν','xi':'ξ','omicron':'ο','pi':'π','rho':'ρ','stigma':'ς',
        'sigma':'σ','tau':'τ','upsilon':'υ','phi':'φ','chi':'χ','psi':'ψ','omega':'ω',

        'vector_or_cross_product':'⨯','medium_small_white_circle':'⚬','hyphen':'-',
        'metrical_breve':'⏑','metrical_long_over_short':'⏒','metrical_short_over_long':'⏓',
        'metrical_two_shorts_joined':'⏖','metrical_long_over_two_shorts':'⏔',
        'metrical_two_shorts_over_long':'⏕',"accent":"´",'sup_1':'¹','sup_2':'²','sup_3':'³','sup_4':'⁴',
        'sup_5':'⁵','sup_6':'⁶','tilda':'~','bar_1':'|','bar_2':'‖',
        'bar_3':'⦀','dotted_bar':'⋮','dashed_bar':'┋'    
    },
    'uppercase':{
        'alpha':'Α','beta':'Β','gamma':'Γ','delta':'Δ','epsilon':'Ε',
        'zeta':'Ζ','eta':'Η','theta':'Θ','iota':'Ι','kappa':'Κ','lambda':'Λ',
        'mu':'Μ','nu':'Ν','xi':'Ξ','omicron':'Ο','pi':'Π','rho':'Ρ','stigma':'ς',
        'sigma':'Σ','tau':'Τ','upsilon':'Υ','phi':'Φ','chi':'Χ','psi':'Ψ','omega':'Ω',

        'vector_or_cross_product':'⨯','medium_small_white_circle':'⚬','hyphen':'-',
        'metrical_breve':'⏑','metrical_long_over_short':'⏒','metrical_short_over_long':'⏓',
        'metrical_two_shorts_joined':'⏖','metrical_long_over_two_shorts':'⏔',
        'metrical_two_shorts_over_long':'⏕',"accent":"´",'sup_1':'¹','sup_2':'²','sup_3':'³','sup_4':'⁴',
        'sup_5':'⁵','sup_6':'⁶','tilda':'~','bar_1':'|','bar_2':'‖',
        'bar_3':'⦀','dotted_bar':'⋮','dashed_bar':'┋'    
    }
};

const kbKeysImages={
    'uppercase': [
        '⇧', 'α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ','ν','ξ',
        'ο','π','ρ','ς','σ','τ','υ','φ','χ','ψ','ω','lowercase'
    ],
    'lowercase':[
        '⇩', 'Α','Β','Γ','Δ','Ε','Ζ','Η','Θ','Ι','Κ','Λ','Μ','Ν','Ξ',
        'Ο','Π','Ρ','ς','Σ','Τ','Υ','Φ','Χ','Ψ','Ω','uppercase'
    ]
}

const magicKeysValues={
    'metric':{
        '[Uu][+][Uu][_]':'⏕', '[Uu][+][Uu][!]':'⏔', '[|][.]':'⋮', '[|][_]':'┋', 
        '[Uu][+][Uu]':'⏖','[|][|][|]':'⦀',
        '[|][|]':'‖', '[Uu][_]':'⏓', '[Uu][!]':'⏒',
        '[Uu]':'⏑', '[Xx]':'⨯', '[Oo]':'⚬', '1':'¹', '2':'²', '3':'³', '4':'⁴', '5':'⁵', '6':'⁶'
    },
    'greek':{
        'A':'Α','B':'Β','G':'Γ','D':'Δ','E':'Ε','Z':'Ζ','H':'Η','Q':'Θ','I':'Ι','K':'Κ','L':'Λ','M':'Μ','N':'Ν','J':'Ξ',
        'O':'Ο','P':'Π','R':'Ρ','[$]':'ς','S':'Σ','T':'Τ','Y':'Υ','F':'Φ','X':'Χ','C':'Ψ','W':'Ω',
        'a':'α','b':'β','g':'γ','d':'δ','e':'ε','z':'ζ','h':'η','q':'θ','i':'ι','k':'κ','l':'λ','m':'μ','n':'ν','j':'ξ',
        'o':'ο','p':'π','r':'ρ','[$]':'ς','s':'σ','t':'τ','y':'υ','f':'φ','x':'χ','c':'ψ','w':'ω'
    }
};

// const MKBD={
//     'vector_or_cross_product':'⨯','medium_small_white_circle':'⚬','hyphen':'-',
//     'metrical_breve':'⏑','metrical_long_over_short':'⏒','metrical_short_over_long':'⏓',
//     'metrical_two_shorts_joined':'⏖','metrical_long_over_two_shorts':'⏔',
//     'metrical_two_shorts_over_long':'⏕','sup_1':'¹','sup_2':'²','sup_3':'³','sup_4':'⁴',
//     'sup_5':'⁵','sup_6':'⁶','bar_1':'|','bar_2':'‖',
//     'bar_3':'⦀','dotted_bar':'⋮','dashed_bar':'┋'
// }

const inverse_case={'uppercase': 'lowercase', 'lowercase': 'uppercase'}

// function getKeyImg(keyID,kbMode){
//     var kbDict={
//         'lowercase':{
//             'alpha':'α','beta':'β','gamma':'γ','delta':'δ','epsilon':'ε',
//             'zeta':'ζ','eta':'η','theta':'θ','iota':'ι','kappa':'κ','lambda':'λ',
//             'mu':'μ','nu':'ν','xi':'ξ','omicron':'ο','pi':'π','rho':'ρ','stigma':'ς',
//             'sigma':'σ','tau':'τ','upsilon':'υ','phi':'φ','chi':'χ','psi':'ψ','omega':'ω',

//         },
//         'uppercase':{
//             'alpha':'Α','beta':'Β','gamma':'Γ','delta':'Δ','epsilon':'Ε',
//             'zeta':'Ζ','eta':'Η','theta':'Θ','iota':'Ι','kappa':'Κ','lambda':'Λ',
//             'mu':'Μ','nu':'Ν','xi':'Ξ','omicron':'Ο','pi':'Π','rho':'Ρ','stigma':'ς',
//             'sigma':'Σ','tau':'Τ','upsilon':'Υ','phi':'Φ','chi':'Χ','psi':'Ψ','omega':'Ω'
//         }
//     };
//     return kbDict[kbMode][keyID];
// }

if(!window.dash_clientside) {window.dash_clientside = {};}
window.dash_clientside.clientside = {
    js_greek_input_line: function(keyID, kbMode, v, z){
        var input_elem=document.getElementById('main_input');
        input_elem.focus();
        var l=kbKeysImages[inverse_case[kbMode]];
        var m;
        if (z=='schemeChoice'||z=='rithmChoice') m='metric';
        else {
            if (z=='srcChoice') m='greek';
            else m='';
        }
        if (keyID.length>1){
            switch (keyID) {
                case 'space':
                case 'mspace':
                    v+=' ';
                    break;
                case 'backspace':
                case 'mbackspace':
                    v=v.slice(0,v.length-1);
                    break;
                case 'magicButton':
                    if (m != ''){
                        for (var x in magicKeysValues[m]){
                            var r = new RegExp(x,'g');
                            v=v.replaceAll(r,magicKeysValues[m][x]);
                        }
                    }
                    break;                    
                case 'changecase':
                    var l= kbKeysImages[kbMode];
                    break;
                default:
                    v+= KBDICT[kbMode][keyID];
            }
        }
        return [v].concat(l);
    }
    // ,
    // js_metric_input_line: function(keyID,v){
    //     var input_elem=document.getElementById('main_input');
    //     input_elem.focus();
    //     if (keyID.length>1){
    //         switch (keyID) {
    //             case 'mspace':
    //                 v+=' ';
    //                 break;
    //             case 'mbackspace':
    //                 v=v.slice(0,v.length-1);
    //                 break;
    //             default:
    //                 v+= MKBD[keyID];
    //         }
    //     }
    //     return v
    // }
}

