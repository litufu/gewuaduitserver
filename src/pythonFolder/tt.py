# -*- coding:utf-8 -*-

import sys
from sqlalchemy import create_engine,and_
from sqlalchemy.orm import sessionmaker
from supplier_natrue import add_supplier_nature
from utils import count_time
from entry_classify import analyse_entry
from entry_test import aduit_entry
from check_entry import check_entry
from importance import get_actual_importance_level
from supplier import save_supplier_to_db
from customer import save_customer_to_db
import pandas as pd



df = pd.read_excel("D:/limin/2016/pz.xlsx", index_col=0)
df.to_excel("D:/limin/2016/pz1.xlsx")

content = '''
<!DOCTYPE html> <html lang="en"> <head> <meta charset="utf-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge,Chrome=1"> <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no"> <meta name="renderer" content="webkit"> <meta name="author" content="leslie"> <title>江苏华兰药用新材料股份有限公司-华国平【工商信息-电话地址-注册信息-信用信息-财务信息】查询-企查查</title> <meta name="keywords" content="江苏华兰药用新材料股份有限公司,江苏华兰药用新材料股份有限公司工商信息,江苏华兰药用新材料股份有限公司招聘,江苏华兰药用新材料股份有限公司地址电话,江苏华兰药用新材料股份有限公司怎么样,江苏华兰药用新材料股份有限公司工资待遇,江苏华兰药用新材料股份有限公司信用信息"> <meta name="description" content="江苏华兰药用新材料股份有限公司怎么样？企查查为您提供江苏华兰药用新材料股份有限公司的最新工商信息、诉讼信息、电话号码、招聘信息、公司简介、公司地址、公司规模、信用信息、财务信息等详细信息，让您在选择江苏华兰药用新材料股份有限公司前能够做到全面了解江苏华兰药用新材料股份有限公司的信用信息。"> <meta name="applicable-device" content="pc"> <link rel="alternate" media="only screen and(max-width: 640px)" href="https://m.qichacha.com/firm_5f981c1538705fe2ec4891565b370edc.html"> <link rel="canonical" href="https://www.qichacha.com/firm_5f981c1538705fe2ec4891565b370edc.html" /> <meta name="mobile-agent" content="format=html5;url=https://m.qichacha.com/firm_5f981c1538705fe2ec4891565b370edc.html"> <link rel="icon" href="/material/theme/chacha/cms/v2/images/favicon.png"> <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/bootstrap.css" type="text/css" /> <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/font-awesome.min.css" type="text/css" /> <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/icon.css" type="text/css" /> <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/font.css" type="text/css" /> <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/app.css?time=1573121164" type="text/css" /> <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/common.css?time=1573121164" type="text/css" /> <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/nuser.css?time=1573121164" type="text/css" /> <link rel="stylesheet" href="/material/theme/chacha/cms/pro/css/simple-line-icons.css" type="text/css" /> <!--[if lt IE 9]>
    <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/app_ie8.css?time=1508428800" type="text/css" />
    <script src="/material/theme/chacha/cms/v2/js/html5shiv.js"></script>
    <script src="/material/theme/chacha/cms/v2/js/respond.js"></script>
    <![endif]--> <script type="text/javascript" src="/material/js/siteconfig.js?time=1573121164"></script> <script src="/material/theme/chacha/cms/v2/js/jquery.min.js"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/qrcode.min.js"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/jquery.scrollTo.js"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/jquery.qrcode.min.js"></script> <script src="/material/theme/chacha/cms/v2/js/bootstrap.js"></script> <script type="text/javascript" src="/material/js/echarts.min.js"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/china.js?time=1508428800"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/chartsUtil.js?time=1573121164"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/kslide.js?time=1573121164"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/searchList.js?time=1573121164"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/phoneSelect.js?time=1573121164"></script> <script src="/material/theme/chacha/cms/v2/js/slimscroll/jquery.slimscroll.min.js"></script> <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/toastr.css?time=1573121164" /> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/moment.js"></script> <script src="/material/theme/chacha/cms/v2/js/toastr.js" type="text/javascript"></script> <script src="/material/theme/chacha/cms/v2/js/custom.js?time=1573121164"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/zhuge.js?time=1573121164"></script> <script type="text/javascript">
        var userId = '';
    var userGroupid = '';
    var freeCompanies = ["887d60f96e7e463ac53f94e8f96feae2","befe52d9753b511b6aef5e33fe00f97d","0b2f5b58208e1d35854f9760fae38be1","4659626b1e5e43f1bcad8c268753216e","cfd79eb5ab631f087ac61e5a3d963e54","5147f91e2fa6efc81b7ff22db6269d2f","y8870a349ef11b2497b0f5c5238334a7","41cacddef5c00110023060dd4268c5ef","8b6954ab68d95dbc08c5510a4aea89e9","c29c4055ec868edecc2220fa224a7c18","649b23c348efa561a79670902e8a7501","4cf1dc2724ff6e483097a878c7ca4e8b","78189c7d652ac1934affde427ac991a0","4abb2712213f465aaa249ab1c9e00def","952d6cd0e3c782fd6cdfa5773307a7bf","f3c7089c90bbd4ad59cda721b4e95c0b","8c2206cb6ba9f7447b81063cf949203b","640a8979aff3fd9f23920af3a6b18d24","450ad1cc2a96add81246a7d9aa42a553","454bc346974f1f7291e6c10373040ff2","0795b537ea095e960d138989bcfa219a","824019145e78e68ff27cd68ddb99e86b","cfd79eb5ab631f087ac61e5a3d963e54","8c977787694d5a833d29786ea56a4e16","ff504aa52e67a5a7e1c49edf46b72247","c9912118e1889a47d7b59a2769db2a52","80f2ee38cd18bec5acf0f6411cee5cf1","d36a8d8d556d1d27438eab610bce0413","64f33caade82c0db342f8fcc5e5a416c","28520655e5af66ff277f13f36fbeb16d","23c507be8d699975625b39c6d0a0f3e6","6e7ea2c0d7465532d3cddebffa4b102a","f1c5372005e04ba99175d5fd3db7b8fc","d025c9ad53fa25c0cc703c9d3d294b36","60f83985cf442a0434e827c0445e7a1f","13de6978d7079ff5471ebe2602bbd8dc","1be64fce7c7de2a7f901b06c0ba43a09","1e8224752286b3fee6a5bfc40587bba1","96efa54feaaf773b4be3381b75457fa1","9da51287f433eb974e5e4e764765582b","cf7f3df5800d6718e85397be2d3a5543","db2019804bd087e9c51919c1ac83a5b1","551a9d96797837ab5c6367f3b0fefaa4","d64949869efaba49a9acc5f3fe75640e","3616afa5ea2ae8c4247d14c1e75a7a63","af1258481a8ed41f8555b079f38c3161","ece76b385263f8ddc4c8ea05e2926fe5","b8effb4a50fe43331c72db049c7a0d0f","4c5df1b087671c1a2dae3ea706f86f17","c4877d95e9a22f9b320a1934f3f576b1","9cce0780ab7644008b73bc2120479d31"];
    var freePeople = ["p0da1fd62398858e47435903170d20f6","pdd3325c48473fcd64180921d82ead80","pceb56d68d90e7b0806f41be5b30465b","p9fa343b3bb5216b246c72aeb77bce0c","p5bc9fe5f2c93301052dc39453855dde","p81f560aded586c166f5014db3919ebd","p4b4fda0151ace817f4c79746530eca1","p5a60350edce8397a6eb99586764df6c","pc127c37072772dabd4865bd62459891","p904b82f5b0df193c45ee2167277281b","pae421fa552b216a2ac67f6168d67a38","p3483c261f318de061fb3ded0508bf90","p208cb12d979ef569739bd8753ce6649","p0fdcfa8108bd10d18026d7a6186e8a0","p0ab2e77de0027adc611b908d12b73ea","pad4ad4c3b995c633a39ae06c899f18a","pbf3da456127e996c276a5bf220c7152","pc464dd4c2d1df467ac4fb6b35dd5a94","pb3cc3d6e608758fad83c053f6f7d8f1","pbfcfb2db5d738323c168f5e3c16db49","pcbfd37ad2a2598da9a6b5de289835dd","pbfd190fa68be5988ff53ae9c1fb75e7","p6abbf243fc5557f96d4488fde8a89f5","p202afa75ec282beabae2dd5d1f8e521","pf38ddce3220b4e7c2c7ead12a534403","pc4eb763297cf4b8076c2e0d2fe64617","p476184110a69c8ab1e6f1bf32506f07","peff4efbd8aaa94d852a42d6bd4f622e","p03d87fd320f2167380bf07ac16794e9","p077472cd738bf6c70d757a42c6acaf4","p2dc826c24f06db3e6cb207b2a494533","p7b171afb629657b151c43bf3e718155","pe19e4c219613e43e5ef8816e3b34291","pf7f4dc246a163ec4a2eedbb67764f7f","paf1c4d41c4c9dcba9a7b1c986957935","pc76b9853c3325d7b5ea9d8af2fa0fca","pd24f0e6c29ec7afe56cac57d665a70b","pfffdf5c707f4ba7162eebd404630418","p51425b4e76d82435b0dfb1192bc5deb","p80a2115e4c716ca032ced9f007af2c8","p8b780c0b5697bb1daa669804aa071d9","p91f92d0f783be4faba5935904f6e2e1","pbaffdb371282141ce912ea1ba440bcd","p50ccd2810b29b8f5ea618cee02ed02e","p7a226f4f0462f27a7ec88903ed5f90a","p33f9ba51dbd068643200f2315655900","pf26740c52b73dbc30c0b8bd40a38021","p441efd3807a065c24de74b5b4be3b5d","pbd14c1a830af087a22e664b211111a2","p089070bd9e914e774ef3e95d00ec5b0","p443d6a190278796f7930982dfe73f42","p2f4391f2600fcc10442c8f22606be20","p146c9f00d63c0fc5e1d4634c917889e","pd260c6712ed49ee88504a64c5ed9482","p347ca283005d596e26b5705fe3e5424","p25fe19b03899303d307235eaa471916","pr51b8951f1049973a8ba758266b6779","p871b2ad73b8b07e3997b0db7fcf9772","p67d2355b8ca06b442eda7b5a55b4803","p226df53c2baa849d6934a9089085ebf","pc0afc496a38fb16121ba654241bee5b","pc4a47cfe2e67199a3c45d9f8c40e1c0","p593208d3aa8e49707325de214a8cb60","p557b82fef8b08e481aadb65085b008b","p04609ece9fe504be41433742c1bf3eb","p522e021cee9336bfb6097250baa3e1b","p568dbf4e82ed6effd2ea1682c7943b8","p089070bd9e914e774ef3e95d00ec5b0","p82222ef85bfd379a8e5226dadc543dd","p684b3f0c79b5dfe6d8a290ba66e798a","p287aa836f4e2c3c6597d09f37731f85","p858a1f2f2e7864fac8d3acce4c8bb8f","p8cb6c16db2ea8fac8ecaadefe35ff8b","p6b2cf613dd4772da8ff3a9575eec8bf","p0b1f20c4c28963ace6eff596cbb7214","pfd208a680dc4871736b7001274ba8f0","pbbefb7a246f4e86a033713e889f9674","pe366442cb673caf54889e6df853e0c0","pf6ea929da129db627bfcf9bf48edc65","p1856f2582e91cf6869be9652cf91512","pde0ba11f9cc81e8e22b89d378dd597b","pe919b2bf2e9c6cdd24d8b63f5969fdd","p1db0b9e274d3e70dd9a2334ad82b93b","p38b6a9f4201932948f613f90ab24cdd","p0e6f9e9a26a0e41c4a3f9be7c062ef2","p9070853c3d33d38134c64a156989284","pbccd0d3eb5ada9952e52772f9e54ebe","p79bb7b0dd3f36e6e5f5100c4e3235a9","pr9c47cb6b2a96048c1d49d1ec72b3c7","p89c2161a36e89cd81bc47424c28ae5b","pae9614885f6fe1df986a5657337915a","p32d88b0b48cd2bbcd9d4f29b1b1670d","p375870fa646d110dde4fbe356f1913e","p0d43bf24ced3d482947792b410b3892","p2766646c26fb8bf53f01c17c0cd1a7e","peabcad582bff5cc35feddb8a2dca458","p9e7818eb8ffc10380ddeb37549c3594","p62f5e7603c2870f0316e439db89d33e","p8bb365678cceb173c3f6645fac32463","pd7d02c68b11c928bc5c5f3f68a43bd8","pd99973e6e867199057f35891f10ece9","p5bc1e3c3f62ed3437786bc969600b9a","pdc2b7a3cc2c414b3910a1d9e116567a","pa884808a0e7526dd17a682739cb38ec","p0b093ef01998ca26f345d4231003a9b","pa85a527d51f75da260083b1cf98da24","p24129f60d16a9d20e70f29452341dec","p507f1693d86036364ec3b5b4d3c0639","p60d00d52bf712741e2fc7f435a31302","p4609f5b766b75d4ab09180fa954da02","p6da28fd74891226f20838f3900fad36","pa43fd5c3172044465f25069df6e61b8","p189c9b0f7e004118b9484f47e6cda68","p96fe6a8b395b31912ecb7e1f41f23b0","pea5ac417585edc0effd7d23406510da","pd57e12ca20e0096dfea61993dfe48f8","p03cf330a686332cfe9cb8f36a8f3ab8","p8ca4283fb80cf988920545e99aef3a4","p1910534b4ae98fea35ddbeb1d61cd44","pb5d99e1912cf2b87f96c7fdaa129ebe","pb6f2f51a297e57acd8a8a161a6a28bc","p131e16ad01343fa580933ad37cd33cb","p70e7789ba2d4e8172cc4fec474711fb","p6609596e149d5bc0201a0b9f4e4fcb7","pb7beff14c56b6f216f92ad95d874f51","pad06603add12c231e78caab20a05f6c","p411cb5d3d6a3399aa210df8845090ea","pf614487a898ad76c39ec0fc65ec3d4f","p954d6bbb51b05a8b3f91e51e79901a9","p5b288352cf3b9499b9271bf888008df","p0ca25440e7114c5974d01d583e52b00","pc747a2d6aaa24efad55793147bc7987","p2a2c9a1417dfff19e607aa3b30787b9","p44cb4832f4146f286a2c5c4ab4ef673","p7cb6f77da9f15766cb65765761c9d19","p38bfd08992f02ba2a136ca892d62899","pd05b697b081dcb4e66719032c2cc760","p61fbfc3a108d8efaf565de1306e23a0","p21c63257afca04e61ff32ac5580572a","p1ec3c35fa9051d8723047b80453ae69","p9d9efeb5aa665dbe66525ced8158f90","pb0489d8530decee9a061f3be5732844","p4bcf05c17b1b0918890fe3a5e64d41f","pfa52806be628929568e0dcbd943d57e","p18da2d9c2244c6dba4180f0d38a7716","p30833a0589ab2f56f93bd113bbaf9bd","pdd9194581da5dda4f700baebc44cc31","pf21af25ef345c47daa9e738732edfa6","pe553922ca919d6a7258c4056e2ab6b7","p7737993e45432ed0e721b28267e058a","p6fb279283ceeba19fe9e85acf4c1f7e","p784a2184d94be1818b6d522b5c8a9d9","pd9751940a8bdcf373ae27804f29c12a","pa313dc90dffce21f98187ca8b1eaa15","p8c945c9f031c2fa391208aeb9a63777","pf1e6aed975eb577cb46d51ac7ec3f14","pb85b223185323f8cc668b7146ddaba9","p4b2c9d74f0a53dc7834fb9aaed58bfd","p84c368f313b4d0808e3fb8ca36e10ad","p917b446e33f719e683fa127465c03bc","p14811e6d3e3c6380ce34dc64d6bb0c2","p325ad0d3c574b124e802f3ad612b7bd","pb46f67ed928d48c6f59af057ca64fcf","pc5e58ea25a0966d860efa862e64a4b3","p0cf2da4ed6ccd9fff31cd232bd3a795","p2bf510b2944458716d0a263913866f1","p2bfa369c340fc42e4c408a98f0a1f26","p4f92d97100bd868d73fa62e9ce00b28","p592a5a06fd6d1ffa4a204e0c499de24","pa289f26dbfa128c37beb57b793edc79","pf410cc5e6bf73d7a117de49a7b1af5e","p2c045fc38d5bec1d438cc581e0f86a4","p89043bad02f62e899855bceb1f7c71b","pr4c963d26e89c8fff17daf449668e16","p8cf7445cd8c5956c7480f1d507b2cd1","p885609c358d14e07fd99d41ed314e99","p57180cc2a70271694f52740d0d9ae1b","p4a6bb86866883881d5f7005f861f7a4","p57153b6ab8750d1dfd32b0c56f398d1","p556225ea3e000a06e4a35f2bdf18481","p1c907e22aaff36740ea8f603b901b32","p412cd235e5252a1c8b90705bf19fbcb","p0b9468faca13fb6100df091d20297f1","pb4e17e90f7c1cfa54560ac4fe041db6","p6c7313d1a025112e8778dfeedc0ffe1","pc491219acf1f61a59c04dea39bedfa5","p5bb4cb536f8904b937650ecbac0b94a","p26b2932ed1a63519bb81e44ba8c104c","pd3f1646db9a01cea29c61c33b9ee617","p64df099fa4661b4d400c5896a39681b","pd923a5cc21dfac7fdbf9dfa9c6fa533","pc97d58fb9ac9bd3836bbe07fdd2735a","p0248c4f7a28bc236748fc4610b5ef1d","p4caa8eb789c5d0fe7d6a88b0dc9000c","p4f2b6e1ae6b40edafecde1c73e85cd2","p056aab2e73f92dbcebd51da8111c1ac","pr894be363cef980d10af39d88a85398","p0794177a7df688a3c779b7408edebf0","pf9ec94f17dc07af1ecd3409f3523f6d","pbb6cbd616af10953b12db428bd7af9d","p7e22dafa4d6ee1193820480fed43953","p067936c7397b739ec6b0d297b95ec06","pr0a8298f7c230bf5fc40124625a7d1c","p8718f47f94756d94d3933ea806b76c3","pf559e9748951e5c469d144da6fd5c8c","p74c5e42ade7e0a0c94badba92f5a66b","p892fd42c420a158abbdb899f7b199c4","p26bf4d581bdf25dd5dce172689be1cf","p5585fa223b46d1250fcadaf6a74bc70","p32c772c9801cf98b711e952902ba2ce","pb92c1a7e84cf6ff79b254154d1eda17","p627634414f75aa172f1623c6d909bb5","pfe71e70a5951f48e2d6be8134a69ab9","p418e3e56998a8e8237a551840a9976d","pa8379689f22cb9c588dadacbac3bd90","p3a8634f7b3ad183f6f31b9123868dce","pr796baa55fffb4891c66c5cadf93242","p686bfc2eccc4011491c9a1ddbc7609e","p1b1e565d80a051007b8d18f17e07e05","p9a719fb3a18f289340fd0c43c356839","p91e374fa50b4648e9911d941ece2b82","p824b008f59b9e5d89842ea9bd529587","pff44c7629a4b0a2bf96eea21a63f1f7","p3fb6d0bed1bd2c96b172f77c97846f4","p1fdaf8e212811fb8edd33781d84b24d","p4150ff74059ca6c582cb6151ff9718b","p10ff32f62339a56dee86d3a362ee8b2","pf28d61dd4cd96570757734940a28c55","pr0ac1235cf5613a979f9c28dc920302","p436160a297843d6312902a0049665d1","p196fb6607ce39e7e2156b254a9e54d0","p283698248c8c18693974f0ed8e2c488","p1910534b4ae98fea35ddbeb1d61cd44"];
</script> <script type="text/javascript">
    var qrcodePolling = false;
    </script> </head> <body> <div style="width: 100%;height: 56px;background: transparent;"></div> <header class="header navi-header box-shadow navi-header-fixed"> <div class="container"> <div class="navi-brand"> <a class="logo" onclick="zhugeTrack('顶栏按钮点击',{'按钮名称':'LOGO'});" href="/"> <img src="/material/theme/chacha/cms/v2/images/logo4.png" class="m-r-sm" alt="企查查"> </a> <span class="zx"> <span class="inner"> <img src="/material/theme/chacha/cms/v2/images/logo_zx_inner.png" alt="企业征信机构备案"> </span> </span> </div> <form class="navi-form" role="search" action="
            /search"> <div class="form-group"> <div class="input-group"> <a id="clearSearchkey" class="clear-searchkey"></a> <input id="headerKey" name="key" class="form-control headerKey" type="text" placeholder="请输入企业名称、人名，产品名等，多关键词用空格隔开" value="江苏华兰药用新材料股份有限公司" autocomplete="off"> <span class="input-group-btn" style="float: left"> <button onclick="" type="submit" class="btn btn-primary">查一下</button> </span> </div> </div> <section class="panel headerKey header-section" id="header-search-list"></section> </form> <script type="text/javascript">
        $('#headerKey').searchList({
            list: '#header-search-list',
            clear: '#clearSearchkey',
                    });
        </script> <script type="text/javascript">
        var pathname_ = window.location.pathname;
        if (pathname_ == '/search_riskinfo' || pathname_ == '/search_intellectualinfo') {
            $('#tpsearch').attr('action', pathname_);
        }
        </script> <ul class="navi-nav pull-right "> <li class="dropdown appli-drop"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'应用'});" href="#" class="dropdown-toggle" data-toggle="dropdown"> <span class="icon-appli" style="display: none"></span> <i class="nav-icon-hot"></i>
                    应用 <i class="caret"></i> </a> <section class="dropdown-menu app-box"> <div class="row m-l-none m-r-none m-t m-b text-center"> <div class="col-xs-12 nav-split" style="margin-top: 0px;"> <label>热门服务</label> <span></span> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'查老赖'});" target="_blank" href="/more_deadbeat" class="header-icon-text"> <div class="nav-icon-new"></div> <span class="m-b-xs block"> <i class="header-icon6"></i> </span> <span>查老赖</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="loginPermision(event);zhugeTrack('顶栏按钮点击',{'应用名称':'风险监控'});" href="/monitor_dynamic" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon1"></i> </span> <span>风险监控</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'千寻地图'});" href="/map" class="header-icon-text"> <i class="nav-icon-hot"></i> <span class="m-b-xs block"> <i class="header-icon2"></i> </span> <span>千寻地图</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'招聘查询'});" target="_blank" href="/more_recruit" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon3"></i> </span> <span>招聘查询</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'大咖搜索'});" target="_blank" href="/company_muhouperson" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon4"></i> </span> <span>大咖搜索</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'行业数据'});" target="_blank" href="https://www.hanghangcha.com" class="header-icon-text"> <div class="nav-icon-hot"></div> <span class="m-b-xs block"> <i class="header-icon5"></i> </span> <span>行业数据</span> </a> </div> </div> <div class="col-xs-12 nav-split"> <label>批量查询</label> <span></span> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'企业'});" href="/more_batchsearch" class="header-icon-text"> <i class="nav-icon-hot"></i> <span class="m-b-xs block"> <i class="header-icon11"></i> </span> <span>企业</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'信用报告'});" href="/more_batch?type=1" class="header-icon-text"> <i class="nav-icon-hot"></i> <span class="m-b-xs block"> <i class="header-icon12"></i> </span> <span>信用报告</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'受益人'});" href="/more_batch?type=2" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon13"></i> </span> <span>受益人</span> </a> </div> </div> <div class="col-xs-12 nav-split"> <label>投融资</label> <span></span> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'创业公司'});" href="/elib_financing" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon21"></i> </span> <span>创业公司</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'投资机构'});" href="/elib_investfirm" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon22"></i> </span> <span>投资机构</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'上市公司'});" href="/elib_ipo" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon23"></i> </span> <span>上市公司</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'园区大全'});" href="/more_zonesearch" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon24"></i> </span> <span>园区大全</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'科创板'});" href="/elib_kcb" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon35"></i> </span> <span>科创板</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'股权服务'});" target="_blank" href="https://www.shareplus.cn/?hmsr=%E4%BC%81%E6%9F%A5%E6%9F%A5&hmpl=&hmcu=&hmkw=&hmci=" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon34"></i> </span> <span>股权服务</span> </a> </div> </div> <div class="col-xs-12 nav-split"> <label>其他服务</label> <span></span> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'接口API'});" target="_blank" href="http://openapi.qichacha.com/?source=websiteHeader" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon32"></i> </span> <span>接口API</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'企业风控'});" target="_blank" href="http://pro.qichacha.com/?source=websiteHeader" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon31"></i> </span> <span>企业风控</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'企业服务'});" target="_blank" href="http://www.qifufu.com/" class="header-icon-text"> <span class="m-b-xs block"> <i class="header-icon33"></i> </span> <span>企业服务</span> </a> </div> </div> <div class="col-xs"> <div class="padder-v"> <a onclick="zhugeTrack('顶栏按钮点击',{'应用名称':'商标注册'});" target="_blank" href="https://www.qccip.com/product/347.html" class="header-icon-text"> <div class="nav-icon-new"></div> <span class="m-b-xs block"> <i class="header-icon36"></i> </span> <span>商标注册</span> </a> </div> </div> </div> </section> </li> <li class="head-line">|</li> <li class="" class="dropdown"> <a rel="nofollow" onclick="zhugeTrack('顶栏按钮点击',{'按钮名称':'APP下载'});" href="/app" class="dropdown-toggle header-qrcode">
                    APP下载
                </a> <section class="dropdown-menu qrcode-box"> <img src="/material/theme/chacha/cms/v2/images/header_qrcode@2x.png?t=3"> </section> </li> <li class="head-line">|</li> <li class=""> <li class=""> <a rel="nofollow" onclick="zhugeTrack('顶栏按钮点击',{'按钮名称':'VIP服务'});" href="/vip">VIP服务</a> </li> </li> <li class="head-line">|</li> <li class=""><a onclick="zhugeTrack('顶栏按钮点击',{'按钮名称':'企业套餐'});" href="/qiye">企业套餐</a></li> <li class="head-line">|</li> <li> <a rel="nofollow" class="navi-btn" onclick="showLoginModal();"> <span class="" >登录 | 注册</span> </a> </li> </ul> </div> </header> <script type="text/javascript" src="/material/js/jquery.cookie.js"></script> <script type="text/javascript" src="/material/js/jquery.validate.min.js"></script> <script type="text/javascript" src="/material/js/jquery.form.min.js"></script> <script type="text/javascript" src="/material/js/global.js?t=1573121164"></script> <style type="text/css"> 
    @media (min-width:960px){
        .modal-dialog {
            width: 960px;
            margin: 30px auto;
        }
        #feedModal .modal-dialog,#shareModal .modal-dialog{
            width: 560px;
            margin: 30px auto;
        }
    }
  #fapiao-title{
      display: none;
  }
  .zhuxiao{
        color: #FD485E;
        text-align: center;
        background: #fff;
        padding: 10px;
        margin-top: -
    }
    .zhuxiao span{
        cursor: pointer;
    }
</style> <div class="container p-t" style="position: relative;"> <div class="m-b-sm"> <a href="/" style="color: #888">首页&nbsp;></a> <a href="/g_JS" style="color: #888">江苏省企业查询&nbsp;></a> <a href="firm_5f981c1538705fe2ec4891565b370edc.html" style="color: #888">江苏华兰药用新材料股份有限公司</a> </div> <div class="panel padder n-s nheader b-a" id="company-top"> <div class="own-switch "> <a class="own-switchback active" href="/firm_5f981c1538705fe2ec4891565b370edc.html" onclick="zhugeTrack('企业主页-企业主页tab',{'企业名称':'江苏华兰药用新材料股份有限公司'});"><div class="zi">企业主页</div></a> <a rel="nofollow" class="own-switchto " href="https://pinpai.qichacha.com/own_5f981c1538705fe2ec4891565b370edc.html" onclick="zhugeTrack('企业主页-品牌主页tab',{'企业名称':'江苏华兰药用新材料股份有限公司'});zhugeTrack('企业主页头部按钮点击',{'按钮名称':'品牌主页'});"><div class="zi">品牌主页</div> <span class="count">1</span> </a> </div> <div class="row"> <div class="logo"> <div class="imgkuang"> <img src="https://co-image.qichacha.com/CompanyImage/5f981c1538705fe2ec4891565b370edc.jpg?x-oss-process=style/qcc_cmp" alt="江苏华兰药用新材料股份有限公司" onerror="this.src='https://co-image.qichacha.com/CompanyImage/default.jpg'"> </div> <div class="m-t-xs"> </div> <div class="company-visit " id="companyVisit">
	浏览量：1万+	<div class="visit-depanel"> <div class="demodal"> <div class="wrap"> <div class="chart-title">近7天的访问量趋势</div> <div class="chart" id="visitChart"> <img class="load" src="/material/theme/chacha/cms/v2/images/preloader.gif"> </div> </div> <div class="foot"> <span class="text-warning">认证后即可查看30天访问记录，去认证自己的企业</span> <a rel="nofollow" class="btn btn-warning pull-right" onclick="zhugeTrack('企业主页-浏览量-认证企业',{'企业名称':'江苏华兰药用新材料股份有限公司'});" href="/company_cert?companykey=5f981c1538705fe2ec4891565b370edc&companyname=%E6%B1%9F%E8%8B%8F%E5%8D%8E%E5%85%B0%E8%8D%AF%E7%94%A8%E6%96%B0%E6%9D%90%E6%96%99%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8" target="_blank">
					认证企业
				</a> </div> </div> </div> </div> <script type="text/javascript">
	$(function(){
		setTimeout(function() {
			visitChart('5f981c1538705fe2ec4891565b370edc','11127');
		}, 350);
		
	})
</script> </div> <div class="content"> <div class="row title jk-tip"> <h1>江苏华兰药用新材料股份有限公司</h1> <a rel="nofollow" onclick="zhugeTrack('企业主页-认证企业',{'企业名称':'江苏华兰药用新材料股份有限公司'});" class="btn-nrenzheng" href="/company_cert?companykey=5f981c1538705fe2ec4891565b370edc&companyname=%E6%B1%9F%E8%8B%8F%E5%8D%8E%E5%85%B0%E8%8D%AF%E7%94%A8%E6%96%B0%E6%9D%90%E6%96%99%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"> <object class="renzheng-warp"> <img src="/material/theme/chacha/cms/v2/images/renzheng_pic.png"> <div>完成企业高级以上认证，您将获得</div> <div class="text-warning">自主完善企业信息、企业品牌、产品推广</div> <div>等11项特权，帮助您的企业获得更多商业机会</div> <a rel="nofollow" href="/company_cert?companykey=5f981c1538705fe2ec4891565b370edc&companyname=%E6%B1%9F%E8%8B%8F%E5%8D%8E%E5%85%B0%E8%8D%AF%E7%94%A8%E6%96%B0%E6%9D%90%E6%96%99%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8" class="btn btn-primary">立即认证</a> </object> </a> </div> <div class="row tags"> <span class="ntag text-success tooltip-br" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="right" data-delay="500" title="企业在通过改制重组后，以集团公司或母公司的形式存在的未上市企业，被称为存续企业。">存续</span> <span><span class="ntag  text-warning tooltip-br" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title=" <span>江阴兰陵瓶塞有限公司</span><br> ">曾用名<i style="position:relative;left:2px;top:-2px;" class="fa fa-sort-desc" aria-hidden="true"></i></span></span> <span class="ntag text-primary" data-trigger="click hover" data-toggle="tooltip" data-placement="bottom" title="从事电子与信息技术、生物工程和新医药技术、新材料及应用技术、先进制造技术、航空航天技术、现代农业技术、新能源与高效节能技术、环境保护新技术、海洋工程技术、核应用技术及与上述十大领域配套的相关技术产品等的一种或多种高新技术及其产品的研究开发、生产和技术服务的企业叫做高新企业。">高新技术企业</span> </div> <div class="dcontent"> <div class="row"> <span class="fc "> <span class="cdes">电话：</span> <span class="cvlu"> <span style="color: #000;"> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">
                                        0510-6897****
                                    </a> </span> <a style="color: #128bed" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('企业主页-更多号码',{'企业名称':'江苏华兰药用新材料股份有限公司'});" class="m-l-sm">
                                        更多号码
                                    </a> <a onclick="zhugeTrack('企业主页-编辑电话',{'企业名称':'江苏华兰药用新材料股份有限公司'});" class="text-primary m-l-sm" data-toggle="modal" data-target="#editContactInfoModal">编辑</a> </span> </span> <span class="cdes">官网：</span> <span class="cvlu "> <a onclick="zhugeTrack('企业主页-查看官网',{'企业名称':'江苏华兰药用新材料股份有限公司'});" href="http://www.hlnpm.com" class="" target="_blank" data-trigger="hover" data-toggle="tooltip" data-placement="right" title="进入官网" data-delay="500" rel="nofollow"> www.hlnpm.com </a> <a class="text-primary m-l-sm" target="_blank" href="/more_certunite?source=firm">认证</a> </span> </div> <div class="row"> <span class="fc "> <span class="cdes">邮箱：</span> <span class="cvlu"> <a onclick="zhugeTrack('企业主页-查看邮箱',{'企业名称':'江苏华兰药用新材料股份有限公司'});" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">
                                     
                                    ***@hlnpm.com
                                </a> <a style="color: #128bed" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();" class="m-l-sm">
                                        更多邮箱
                                </a> </span> </span> <span class="cdes">地址：</span><span class="cvlu"> <a onclick="showMapModal('江阴市临港新城申港镇澄路1488号','无锡市');zhugeTrack('企业主页-查看地址',{'企业名称':'江苏华兰药用新材料股份有限公司'});" data-trigger="hover" data-toggle="tooltip" data-placement="right" title="查看地址" data-delay="500"> 江阴市临港新城申港镇澄路1488号</a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('企业主页-附近企业',{'企业名称':'江苏华兰药用新材料股份有限公司'});" style="color: #128bed" class="m-l-sm"> 附近企业</a> </span> </div> <div class="row"> <span class="cdes">简介：</span> <span class="cvlu">企 业 简 介
江苏华兰药用新材料股份有限公司（原江阴兰陵瓶塞有限公司）位于江苏省江阴市临港新城申港镇澄路14… <a onclick="zhugeTrack('企业主页-查看简介',{'企业名称':$('#companyname').val()});" style="color: #128bed" data-toggle="modal" data-target="#jianjieModal">查看详情</a></span> </div> <div class="dcert"> <a rel="nofollow" onclick="zhugeTrack('企业主页-认证企业',{'企业认证类型':'未认证'});" class="text-warning pull-right" href="/company_cert?companykey=5f981c1538705fe2ec4891565b370edc&companyname=%E6%B1%9F%E8%8B%8F%E5%8D%8E%E5%85%B0%E8%8D%AF%E7%94%A8%E6%96%B0%E6%9D%90%E6%96%99%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8">编辑企业信息</a> </div> </div> <div class="row dongtai dongtai3  "> <a class="oxin" onclick="zhugeTrack('企业主页-查看产品信息',{'企业名称':'江苏华兰药用新材料股份有限公司'});" href="/product_85dd89bb-9d68-4333-8d38-ebed99920320.html"> <div class="img"><img src="https://img.qichacha.com/Product/85dd89bb-9d68-4333-8d38-ebed99920320.jpg"></div> <div class="pull-left"> <div> <span class="cdes">产品信息：</span> <span class="cvlu">华兰药用</span> </div> <div> <span class="text-gray">融资历程 <span class="text-primary">0</span></span> <span class="text-gray m-l-xs">竞品数量 <span class="text-primary">20</span></span> </div> </div> </a> <a class="oxin" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('企业主页-查看股权穿透图',{'企业名称':'江苏华兰药用新材料股份有限公司'});"> <div class="img"><img src="https://co-image.qichacha.com/CompanyImage/5f981c1538705fe2ec4891565b370edc.jpg?x-oss-process=style/qcc_cmp"></div> <div class="pull-left"> <div> <span class="">股权穿透图</span> </div> <div> <span class="text-gray">挖掘深层股权结构</span> </div> </div> </a> <a class="oxin" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('企业主页-查看企业图谱',{'企业名称':'江苏华兰药用新材料股份有限公司'});"> <div class="img"><img src="https://co-image.qichacha.com/CompanyImage/5f981c1538705fe2ec4891565b370edc.jpg?x-oss-process=style/qcc_cmp"></div> <div class="pull-left"> <div> <span class="">企业图谱</span> </div> <div> <span class="text-gray">企业信息一图掌控</span> </div> </div> <span class="icon-new"></span> </a> </div> </div> <div class="company-action"> <a onclick="$('#loginModal').modal('show');getCaptcha();zhugeTrack('企业主页-监控企业',{'企业名称':'江苏华兰药用新材料股份有限公司'});" class="c_iconDt2 ca_jk" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title="免费监控100家企业、100位老板，为您每日推送<br/>超过60个维度的风险信息，不再错过重要动态"> <span></span>监控风险
                    </a> <a onclick="zhugeTrack('企业主页-递名片',{'企业名称':'江苏华兰药用新材料股份有限公司'});" data-toggle="modal" data-target="#loginModal" class="c_iconDt2 ca_card"> <span></span>递名片
                </a> <a  data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('企业主页-做笔记',{'企业名称':'江苏华兰药用新材料股份有限公司'});" class="c_iconDt2 ca_contact"> <span></span>笔记 <em id="nNodeCount"></em> </a> <a data-toggle="modal" data-target="#loginModal" onclick="pageAddCompare('5f981c1538705fe2ec4891565b370edc');zhugeTrack('企业主页-对比企业',{'企业名称':'江苏华兰药用新材料股份有限公司'});" class="c_iconDt2 ca_compare"> <span></span>对比
                </a> <a id="follow" data-flag="0" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('企业主页-关注企业',{'企业名称':'江苏华兰药用新材料股份有限公司'});" class="c_iconDt2 ca_focus" title="关注公司"> <span></span>关注
                </a> <p class="refs" title="上次更新日期：1时33分钟前"> <a class="m_bt_refresh" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('企业主页-更新数据',{'企业名称':'江苏华兰药用新材料股份有限公司'});"> </a> 1时33分钟前更新
                </p> </div> </div> <div class="company-btoolbar clearfix"> <div id="hotNewsWrap" style="display: none;"> <div class="text-gray pull-left">热点新闻：</div> <div class="hot-news" id="hotNews"> </div> </div> <div class="pull-right"> <a onclick="zhugeTrack('企业主页头部按钮点击',{'按钮名称':'手机查看'});" class="bar-btn phoneviewBtn"> <span class="bar-icon bar-icon-app"></span>手机查看
            <div class="bar-phoneview" data-keyno="5f981c1538705fe2ec4891565b370edc" data-name="江苏华兰药用新材料股份有限公司"> <div class="cname">江苏华兰药用新材料股份有限公司</div> <div class="wrap"> <div class="qrcode"></div> <img class="phone-ic" src="/material/theme/chacha/cms/v2/images/phoneview_ic.png"> </div> <div class="text"> <span class="text-primary">微信</span>或<span class="text-primary">企查查APP</span> 扫一扫查看详情
    	
    </div> </div> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('企业主页头部按钮点击',{'按钮名称':'发票抬头'});" class="bar-btn"> <span class="bar-icon bar-icon-fp"></span>发票抬头
        </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('企业主页头部按钮点击',{'按钮名称':'下载报告'});" class="bar-btn"> <span class="bar-icon bar-icon-report"></span>下载报告
        </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('企业主页头部按钮点击',{'按钮名称':'信息纠错'});" class="bar-btn"> <span class="bar-icon bar-icon-feedback"></span>信息纠错
        </a> </div> </div> <script type="text/javascript">
	$(function(){
                setPhoneview()
        setHotNews('5f981c1538705fe2ec4891565b370edc','江苏华兰药用新材料股份有限公司');
        	})
</script> </div> <div class="modal fade" id="jianjieModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button class="close" type="button" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="myModalLabel">公司简介</h4> </div> <div class="modal-body"> <div class="m-t-sm m-b-sm"> <pre>企 业 简 介
江苏华兰药用新材料股份有限公司（原江阴兰陵瓶塞有限公司）位于江苏省江阴市临港新城申港镇澄路1488号，成立于1992年，经过二十年的不懈努力，现已发展成为一家实力雄厚、品种齐全、技术领先、规模优势显着的专业生产直接或间接接触药物包装材料的现代化高新技术企业。2010年实现销售收入57771万元，利税6379万元。连续叁年列入江阴百强企业。2009年公司被纳入2009中国医疗健康产业最具投资价值企业TOP100。
公司主要从事输液、冻干、粉针、小水针、采血、中药复方制剂用各类“华兰”牌胶塞和软袋接口叁组件、塑瓶接口叁组件、塑料输液容器用聚异戊二烯橡胶垫片等的制造和销售。
华兰股份目前注册资本为1.1亿元人民币，总资产逾6亿元。拥有两家全资子公司：重庆市涪陵叁海兰陵有限责任公司——为响应国家支援西部开发，1998年，公司出资与重庆长丰通讯有限公司共同投资组建重庆市涪陵叁海兰陵责任有限公司。2002年7月，由江阴兰陵瓶塞有限公司和江阴硅氟塑料厂整体收购。2009年改制成为江苏华兰药用新材料股份有限公司全资法人控股公司，是华兰股份旗下专业从事药用丁基橡胶瓶塞研究和生产的核心企业，现已成为西部地区规模最大的药用丁基橡胶瓶塞制造企业；江苏华杨医疗科技有限公司——华兰股份旗下主要从事生物制品和二类6809泌尿肛肠微创外科手术器械的研究、开发。
华兰发展过程中一直坚持“华兰产品等于药品，华兰责任安全有效”的质量方针，把产品质量作为企业第一生存法则， 1998年，公司率先在行业内通过ISO9001质量体系认证，2003年，公司作为药用胶塞行业唯一代表参与起草了由中国医药包装协会组织的《药品包装实用手册》，得到行业的广泛应用。公司华兰牌注射液用卤化丁基橡胶塞获江苏名牌产品称号，自主知识产权产品新型复膜药用丁基胶塞评国家四部委评为国家重点新产品。
在二十年的经营过程中，华兰逐渐形成良好的销售理念，公司以“有诚就有成”的理念与国内外客户进行业务合作，优质的产品、良好的服务使华兰股份在市场上树立了良好的形象，赢得广大客户的认可与信赖，公司的销售网络遍及世界各地并成功进军意大利、叙利亚、埃及、越南、巴基斯坦等国家。2010年度，全国80%药厂都和公司有业务往来，其中建立稳定合作的药厂有800多家。
在经营活动中，公司树立了“股东利益最大化，社会责任永久化，客户利益市场化”的经营理念。一直以来，公司高度重视构建自身的人才优势，不断吸引高层次人才加盟。在全国民营企业中，率先获准成立了药用包装材料研究所，与国内一家知名高分子材料学府建立了校企合作，并与南京航空航天大学经济与管理学院合作，将公司定为其就业实践基地，为企业的创新发展积蓄后备力量。
在企业管理中，公司不断寻求新的突破，2003年9月，为适应市场的激烈竞争，公司全面推行GMP管理，在保证生产正常进行的情况下，把 GMP 各项管理落实到具体的工作任务中去，使之不断科学化、标准化、规范化；2004年公司做出又一重大举措，全面启动ERP项目，企业在信息化管理上又迈出坚实的一步。
公司在发展壮大的同时，时刻不忘积极投身于社会公益福利事业和科学、教育、文化、卫生事业当中，公司设立华兰“扶贫帮困”基金200万元，每年向江阴慈善总会定额支付16万元，直至交满200万元。公司领导充分认识科学知识的重要性，尽其所能，捐赠江阴市二中10万元资金，与申港镇贫困学生华香同学结对助学，助贫困学生顺得完成学业。公司以民营科技企业的身份赞助的江阴“南北结对”活动共资助5名贫困学生等。
2008年，公司被江苏省科技厅、财政厅、国税局、地税局认定为高新技术企业。2009年，华兰股份引入建银国际医疗产业基金等一批战略投资者，成功完成股份制改造。2010年，公司与中投证券签署辅导、保荐协议，正式启动IPO进程。
江苏华兰药用新材料股份有限公司将始终以“以股东利益最大化、社会责任永久化、客户利益市场化”的公司宗旨，坚持“华兰产品等于药品，华兰产品安全有效”的质量方针，深化“诚信为本，人文团队，勇于创新，铸造品牌” 的经营理念，不断推动企业科技进步，力争早日进入世界行业前叁名。</pre> </div> </div> <div class="modal-footer"> <button  type="button" data-dismiss="modal" class="btn btn-primary">确定</button> </div> </div> </div> </div> </div> <div class="container m-t"> <div class="company-certinfo risk-qingbao"> <div class="risk-panel b-a"> <a data-trigger="hover" class="pull-right" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title="自身风险，聚合该公司自身存在的风险信息，其中包含：<br> 警示信息：裁判文书，严重违法，经营异常，行政处罚，税务行政处罚，环保处罚，动产抵押，土地抵押，税收违法，股权冻结，司法拍卖，股权出质，开庭公告；<br> 高风险信息：失信被执行人，被执行人。<br><br> 关联风险，挖掘企业的关联人（如法定代表人，自然人股东，主要人员）和关联公司（如企业股东，投资公司，分公司）风险。其中包含：<br> 关联人风险：失信被执行人和被执行人信息；<br> 关联公司风险：同企业自身风险信息。<br><br>  提示信息，法定代表人变更，大股东变更；<br><br>说明：风险扫描中的数据是基于公开信息通过风险模型大数据分析后的结果，仅供用户参考，并不代表企查查的任何明示、暗示之观点或保证。若因参考、使用该信息造成损失的，由用户自行负责，企查查不承担任何责任。"><i class="m_question"></i></a> <img src="/material/theme/chacha/cms/v2/images/risk_title@2x.png"> <span class="tl"> <a  onclick="showVipModal('风险扫描','成为VIP会员 即可查看企业自身风险和关联风险','fxsm','查看样例公司','/firm_9cce0780ab7644008b73bc2120479d31.shtml');zhugeTrack('开通VIP',{'弹窗来源':'自身风险'});">自身风险
                <span class="text-danger">16</span></a> <a  onclick="showVipModal('风险扫描','成为VIP会员 即可查看企业自身风险和关联风险','fxsm','查看样例公司','/firm_9cce0780ab7644008b73bc2120479d31.shtml');zhugeTrack('开通VIP',{'弹窗来源':'关联风险'});">关联风险 <span class="text-danger">56</span></a> <a  onclick="showVipModal('风险扫描','成为VIP会员 即可查看企业自身风险和关联风险','fxsm','查看样例公司','/firm_9cce0780ab7644008b73bc2120479d31.shtml');zhugeTrack('开通VIP',{'弹窗来源':'提示信息'});">提示信息
                <span class="text-gray">4</span></a> </span> <a onclick="showVipModal('风险扫描','成为VIP会员 即可查看企业自身风险和关联风险','fxsm','查看样例公司','/firm_9cce0780ab7644008b73bc2120479d31.shtml');zhugeTrack('企业主页头部按钮点击',{'按钮名称':'风险扫描-查看风险'});" class="btn btn-danger pull-right">查看风险</a> </div> <div class="qingbao-panel b-a"> <img src="/material/theme/chacha/cms/v2/images/qingbao_title@2x.png?time=1573121164"> <div class="qingbao-scrollinfo" id="qingbaoScrollinfo"> <a rel="nofollow" class="item" onclick="zhugeTrack('企业主页头部按钮点击',{'按钮名称':'企业动态-动态标题'});" href="/company_intelligence?keyno=5f981c1538705fe2ec4891565b370edc&companyname=%E6%B1%9F%E8%8B%8F%E5%8D%8E%E5%85%B0%E8%8D%AF%E7%94%A8%E6%96%B0%E6%9D%90%E6%96%99%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"> <span class="m-r">2019-01-08</span>
                                新增
                                                <span class="text-danger">裁判文书</span> </a> <a rel="nofollow" class="item" onclick="zhugeTrack('企业主页头部按钮点击',{'按钮名称':'企业动态-动态标题'});" href="/company_intelligence?keyno=5f981c1538705fe2ec4891565b370edc&companyname=%E6%B1%9F%E8%8B%8F%E5%8D%8E%E5%85%B0%E8%8D%AF%E7%94%A8%E6%96%B0%E6%9D%90%E6%96%99%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"> <span class="m-r">2017-12-10</span>
                                变更
                                                <span class="text-primary">对外投资</span> </a> <a rel="nofollow" class="item" onclick="zhugeTrack('企业主页头部按钮点击',{'按钮名称':'企业动态-动态标题'});" href="/company_intelligence?keyno=5f981c1538705fe2ec4891565b370edc&companyname=%E6%B1%9F%E8%8B%8F%E5%8D%8E%E5%85%B0%E8%8D%AF%E7%94%A8%E6%96%B0%E6%9D%90%E6%96%99%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"> <span class="m-r">2017-11-29</span>
                                新增
                                                <span class="text-primary">股权出质</span> </a> <a rel="nofollow" class="item" onclick="zhugeTrack('企业主页头部按钮点击',{'按钮名称':'企业动态-动态标题'});" href="/company_intelligence?keyno=5f981c1538705fe2ec4891565b370edc&companyname=%E6%B1%9F%E8%8B%8F%E5%8D%8E%E5%85%B0%E8%8D%AF%E7%94%A8%E6%96%B0%E6%9D%90%E6%96%99%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"> <span class="m-r">2017-11-29</span>
                                新增
                                                <span class="text-primary">股权出质</span> </a> <a rel="nofollow" class="item" onclick="zhugeTrack('企业主页头部按钮点击',{'按钮名称':'企业动态-动态标题'});" href="/company_intelligence?keyno=5f981c1538705fe2ec4891565b370edc&companyname=%E6%B1%9F%E8%8B%8F%E5%8D%8E%E5%85%B0%E8%8D%AF%E7%94%A8%E6%96%B0%E6%9D%90%E6%96%99%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"> <span class="m-r">2017-11-29</span>
                                变更
                                                <span class="text-primary">工商信息</span> </a> </div> <a rel="nofollow" onclick="zhugeTrack('企业主页头部按钮点击',{'按钮名称':'企业动态-查看动态'});" href="/company_intelligence?keyno=5f981c1538705fe2ec4891565b370edc&companyname=江苏华兰药用新材料股份有限公司" class="btn btn-primary pull-right">查看动态</a> </div> </div> <script type="text/javascript">
    $(function() {
        qingbaoCarousel();
    })

</script> <div class="row"> <div class="col-sm-9 no-padding-right"> <header style="height: 44px;position: relative;"> <div class="own-switch fixed"> <a class="own-switchback active" href="/firm_5f981c1538705fe2ec4891565b370edc.html" onclick="zhugeTrack('企业主页-企业主页tab',{'企业名称':'江苏华兰药用新材料股份有限公司'});"><div class="zi">企业主页</div></a> <a rel="nofollow" class="own-switchto " href="https://pinpai.qichacha.com/own_5f981c1538705fe2ec4891565b370edc.html" onclick="zhugeTrack('企业主页-品牌主页tab',{'企业名称':'江苏华兰药用新材料股份有限公司'});zhugeTrack('企业主页头部按钮点击',{'按钮名称':'品牌主页'});"><div class="zi">品牌主页</div> <span class="count">1</span> </a> </div> <div class="company-nav " style="overflow: hidden;"> <div class="company-nav-tab                                                     current                        "> <a class="company-nav-head" onclick="" href="/cbase_5f981c1538705fe2ec4891565b370edc" rel="nofollow"><h2>基本信息</h2> <span>78</span></a> <div class="company-nav-items"> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">查查图谱
                                                                <span class="text-primary"></span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">工商信息
                                                                <span class="text-primary"></span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">历史工商信息
                                                                <span class="text-primary"></span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">股东信息
                                                                <span class="text-primary">38</span> </a> <span>历史股东 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">股权穿透图
                                                                <span class="text-primary"></span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">主要人员
                                                                <span class="text-primary">12</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">历史高管
                                                                <span class="text-primary">9</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">对外投资
                                                                <span class="text-primary">6</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">历史对外投资
                                                                <span class="text-primary">1</span> </a> <span>变更记录 <span>0</span></span> <span>总公司 <span>0</span></span> <span>分支机构 <span>0</span></span> <span>企业公示 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">关联图谱
                                                                <span class="text-primary"></span> </a> <span>建筑资质 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">最终受益人
                                                                <span class="text-primary">2</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">实际控制人
                                                                <span class="text-primary"></span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">控股企业
                                                                <span class="text-primary">6</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">财务简析
                                                                <span class="text-primary"></span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">同业分析
                                                                <span class="text-primary"></span> </a> </div> </div> <div class="company-nav-tab                                                                             "> <a class="company-nav-head" onclick="" href="/csusong_5f981c1538705fe2ec4891565b370edc" ><h2>法律诉讼</h2> <span>15</span></a> <div class="company-nav-items"> <span>被执行人 <span>0</span></span> <span>历史被执行人 <span>0</span></span> <span>失信信息 <span>0</span></span> <span>历史失信信息 <span>0</span></span> <span>终本案件 <span>0</span></span> <span>限制高消费 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">裁判文书
                                                                <span class="text-danger">12</span> </a> <span>历史裁判文书 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">法院公告
                                                                <span class="text-danger">1</span> </a> <span>历史法院公告 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">开庭公告
                                                                <span class="text-danger">2</span> </a> <span>历史开庭公告 <span>0</span></span> <span>送达公告 <span>0</span></span> <span>股权冻结 <span>0</span></span> <span>历史股权冻结 <span>0</span></span> <span>立案信息 <span>0</span></span> </div> </div> <div class="company-nav-tab                                                                             "> <a class="company-nav-head" onclick="" href="/crun_5f981c1538705fe2ec4891565b370edc" ><h2>经营状况</h2> <span>343</span></a> <div class="company-nav-items"> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">行政许可
                                                                <span class="text-primary">4</span> </a> <span>历史行政许可 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">税务信用
                                                                <span class="text-primary">3</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">招投标
                                                                <span class="text-primary">1</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">招聘
                                                                <span class="text-primary">217</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">财务总览
                                                                <span class="text-primary">1</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">进出口信用
                                                                <span class="text-primary">1</span> </a> <span>微信公众号 <span>0</span></span> <span>主要指标 <span></span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">利润表
                                                                <span class="text-primary"></span> </a> <span>资产负债表 <span></span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">现金流量表
                                                                <span class="text-primary"></span> </a> <span>微博 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">新闻舆情
                                                                <span class="text-primary">46</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">公告研报
                                                                <span class="text-primary">67</span> </a> <span>地块公示 <span>0</span></span> <span>购地信息 <span>0</span></span> <span>土地转让 <span>0</span></span> <span>债券信息 <span>0</span></span> <span>抽查检查 <span>0</span></span> <span>电信许可 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">供应商
                                                                <span class="text-primary">1</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">客户
                                                                <span class="text-primary">2</span> </a> <span>信用评级 <span>0</span></span> <span>双随机抽查 <span>0</span></span> </div> </div> <div class="company-nav-tab                                                                             "> <a class="company-nav-head" onclick="" href="/cfengxian_5f981c1538705fe2ec4891565b370edc" ><h2>经营风险</h2> <span>21</span></a> <div class="company-nav-items"> <span>经营异常 <span>0</span></span> <span>严重违法 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">股权出质
                                                                <span class="text-danger">14</span> </a> <span>历史股权出质 <span>0</span></span> <span>股权质押 <span>0</span></span> <span>行政处罚 <span>0</span></span> <span>历史行政处罚 <span>0</span></span> <span>环保处罚 <span>0</span></span> <span>税收违法 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">动产抵押
                                                                <span class="text-danger">4</span> </a> <span>历史动产抵押 <span>0</span></span> <span>清算信息 <span>0</span></span> <span>司法拍卖 <span>0</span></span> <span>注销备案 <span>0</span></span> <span>破产重组 <span>0</span></span> <span>询价评估 <span>0</span></span> <span>土地抵押 <span>0</span></span> <span>简易注销 <span></span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">公示催告
                                                                <span class="text-danger">3</span> </a> <span>欠税公告 <span>0</span></span> </div> </div> <div class="company-nav-tab                                                                             "> <a class="company-nav-head" onclick="" href="/creport_5f981c1538705fe2ec4891565b370edc" ><h2>企业发展</h2> <span>27</span></a> <div class="company-nav-items"> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">企业年报
                                                                <span class="text-primary">6</span> </a> <span>融资信息 <span>0</span></span> <span>投资机构 <span>0</span></span> <span>核心人员 <span></span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">企业业务
                                                                <span class="text-primary">1</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">竞品信息
                                                                <span class="text-primary">20</span> </a> <span>私募基金 <span></span></span> </div> </div> <div class="company-nav-tab                                                                             "> <a class="company-nav-head" onclick="" href="/cassets_5f981c1538705fe2ec4891565b370edc" ><h2>知识产权</h2> <span>155</span></a> <div class="company-nav-items"> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">商标信息
                                                                <span class="text-primary">3</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">专利信息
                                                                <span class="text-primary">120</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">证书信息
                                                                <span class="text-primary">30</span> </a> <span>作品著作权 <span>0</span></span> <span>软件著作权 <span>0</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">网站信息
                                                                <span class="text-primary">2</span> </a> </div> </div> <div class="company-nav-tab                                                                             "> <a class="company-nav-head viptab" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()"><h2>历史信息</h2> <span>11</span></a> <div class="company-nav-items"> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">工商信息
                                                                <span class="text-primary"></span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">历史高管
                                                                <span class="text-primary">9</span> </a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">对外投资
                                                                <span class="text-primary">1</span> </a> <span>历史股东 <span>0</span></span> <span>失信信息 <span>0</span></span> <span>被执行人 <span>0</span></span> <span>法院公告 <span>0</span></span> <span>裁判文书 <span>0</span></span> <span>行政处罚 <span>0</span></span> <span>动产抵押 <span>0</span></span> <span>开庭公告 <span>0</span></span> <span>股权出质 <span>0</span></span> <span>行政许可 <span>0</span></span> <span>股权冻结 <span>0</span></span> </div> </div> </div> </header> <div class="data_div_login"> <div class="base_info"></div> <div class="current"><a id="base_title"></a></div> <section class="panel b-a clear m_dataTab"> <div class="panel-body" style="padding-top: 5px;"> <a href="javascript:;" onclick="boxScrollNew('#qccGraph');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-查查图谱'});" class="btn btn-sm btn-default m-t-sm  m-r-sm" style="white-space:nowrap;">
              查查图谱
          </a> <a href="javascript:;" onclick="boxScrollNew('#Cominfo');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-工商信息'});" class="btn btn-sm btn-default m-t-sm  m-r-sm" style="white-space:nowrap;">
              工商信息          </a> <a href="javascript:;" onclick="boxScrollNew('#partnern');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-股东信息'});" class="btn btn-sm btn-default m-t-sm  m-r-sm" style="white-space:nowrap;">
                  股东信息&nbsp;38
              </a> <a href="javascript:;" onclick="boxScrollNew('#guquan');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-股权穿透图'});" class="btn btn-sm btn-default m-t-sm  m-r-sm" style="white-space:nowrap;">
              股权穿透图
          </a> <a href="javascript:;" onclick="boxScrollNew('#Mainmember');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-主要人员'});" class="btn btn-sm btn-default m-t-sm    m-r-sm" style="white-space:nowrap;">
                  主要人员&nbsp;12
              </a> <a href="javascript:;" onclick="boxScrollNew('#touzilist');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-对外投资'});" class="btn btn-sm btn-default m-t-sm  m-r-sm" style="white-space:nowrap;">
                  对外投资&nbsp;6
              </a> <a href="javascript:;" class="btn btn-sm btn-default m-t-sm  m-r-sm c_disable" style="white-space:nowrap;cursor: default">
                总公司&nbsp;0
            </a> <a href="javascript:;" class="btn btn-sm btn-default  m-r-sm m-t-sm   c_disable" style="white-space:nowrap;cursor: default">
                  分支机构&nbsp;0
              </a> <a href="javascript:;" class="btn btn-sm btn-default m-t-sm  m-r-sm c_disable" style="white-space:nowrap;cursor: default">
                企业公示&nbsp;0
            </a> <a href="javascript:;" class="btn btn-sm btn-default m-t-sm  m-r-sm c_disable" style="white-space:nowrap;cursor: default">
                  建筑资质&nbsp;0 <span class="icon-new"></span> </a> <a href="javascript:;" class="btn btn-sm btn-default m-t-sm  m-r-sm c_disable" style="white-space:nowrap;cursor: default">
                  变更记录&nbsp;
              </a> <a href="javascript:;" onclick="boxScrollNew('#Comintroduce');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-公司简介'});" class="btn btn-sm btn-default m-t-sm   m-r-sm" style="white-space:nowrap;">
                  公司简介&nbsp;
              </a> <a href="javascript:;" onclick="boxScrollNew('#syrlist');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-最终受益人'});" class="btn btn-sm btn-default m-t-sm   m-r-sm" style="white-space:nowrap;">
                  最终受益人&nbsp;2 
              </a> <a href="javascript:;" onclick="boxScrollNew('#kzrtupu');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-实际控制人'});" class="btn btn-sm btn-default m-t-sm   m-r-sm" style="white-space:nowrap;">
                  实际控制人 <span class="icon-new"></span> </a> <a href="javascript:;" onclick="boxScrollNew('#holdcolist');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-控股企业'});" class="btn btn-sm btn-default m-r-sm m-t-sm" style="white-space:nowrap;">
                  控股企业&nbsp;6 
              </a> <a href="javascript:;" onclick="boxScrollNew('#cwjx');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-财务简析'});" class="btn btn-sm btn-default m-t-sm  m-r-sm" style="white-space:nowrap;">
                  财务简析  
              </a> <a href="javascript:;" onclick="boxScrollNew('#thyfx');zhugeTrack('企业主页内容点击',{'点击来源':'快捷入口','数据维度':'基本信息-同业分析'});" class="btn btn-sm btn-default m-t-sm  m-r-sm" style="white-space:nowrap;">
                  同业分析</a> </div> </section> <section class="panel b-a" id="qccGraph"> <div class="tcaption"> <h3 class="title">查查图谱</h3> <span class="watermark"></span> </div> <div class="clearfix"> <a class="base-graphsl" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()"> <div class="img"> <img src="/material/theme/chacha/cms/v2/images/graphsl_1.png" alt="企业图谱"> </div> <div class="text">企业图谱<span class="icon-new m-l-xs m-t-xs"></span></div> </a> <a class="base-graphsl" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()"> <div class="img"> <img src="/material/theme/chacha/cms/v2/images/graphsl_2.png" alt="企业受益股东"> </div> <div class="text">企业受益股东<span class="icon-new m-l-xs m-t-xs"></span></div> </a> <a class="base-graphsl" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()" > <div class="img"> <img src="/material/theme/chacha/cms/v2/images/graphsl_3.png" alt="股权结构图"> </div> <div class="text">股权结构图</div> </a> <a class="base-graphsl" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()"> <div class="img"> <img src="/material/theme/chacha/cms/v2/images/graphsl_4.png" alt="股权穿透图"> </div> <div class="text">股权穿透图</div> </a> <a class="base-graphsl" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()"> <div class="img"> <img src="/material/theme/chacha/cms/v2/images/graphsl_5.png" alt="关联图谱"> </div> <div class="text">关联图谱</div> </a> <a class="base-graphsl" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()"> <div class="img"> <img src="/material/theme/chacha/cms/v2/images/graphsl_6.png" alt="实际控制人"> </div> <div class="text">实际控制人</div> </a> </div> </section> <section class="panel b-a base_info" id="Cominfo"> <div class="tcaption"> <h3 class="title">工商信息</h3> <a onclick="zhugeTrack('企业主页-工商信息-查看工商官网快照',{'企业名称':'江苏华兰药用新材料股份有限公司'});" class="text-primary kz_anim" href="/snapshoot_5f981c1538705fe2ec4891565b370edc.html" target="_blank">
                查看工商官网快照
            </a> <span class="thist">（查看更多<a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">历史工商信息</a>）</span> <span class="watermark"></span> </div> <div class="prot-gltu" id="protGltu"></div> <table class="ntable"> <tr> <td width="20%" class="tb" rowspan="2"> 
                                                  法定代表人
                                        </td> <td width="30%" rowspan="2"> <div class="boss-td"> <div class="clearfix" style="min-height: 76px;padding-top: 8px;overflow: hidden;"> <div class="pull-left bheadimgkuang"> <span class="usericon boss color-2" first-letter="华"></span> </div> <div class="bpen"> <a href="/pl_ped4659e89d457c7f2a22fa1fac34c98.html" class="bname"><h2 class="seo font-20">华国平</h2></a> <a class="btn-touzi pull-left" onclick="relatedList(1,'ped4659e89d457c7f2a22fa1fac34c98','华国平');zhugeTrack('关联企业按钮点击',{'按钮位置':'工商信息','关联目标':'华国平'});">他关联6家企业 > </a> </div> </div> </div> </td> <td width="20%" class="tb"> 注册资本 </td> <td width="30%">  10100万元人民币  </td> </tr> <tr> <td width="20%" class="tb"> 实缴资本 </td> <td width="30%"> 10100万元人民币 </td> </tr> <tr> <td class="tb">经营状态</td> <td class="">
                 存续（在营、开业、在册）             </td> <td class="tb" width="18%">成立日期</td> <td class="">
                1992-06-04
            </td> </tr> <tr> <td class="tb">统一社会信用代码</td> <td class="">
                913202006079820552
            </td> <td class="tb">纳税人识别号</td> <td class="">
                913202006079820552
            </td> </tr> <tr> <td class="tb">注册号</td> <td class="">
                320281400006822
            </td> <td class="tb" width="15%">组织机构代码</td> <td class="">
                60798205-5
            </td> </tr> <tr> <td class="tb">企业类型</td> <td class="">
                股份有限公司(非上市、自然人投资或控股)
            </td> <td class="tb">所属行业</td> <td class="">
                制造业
            </td> </tr> <tr> <td class="tb">核准日期</td> <td class="" style="max-width:301px;">
                2019-06-28
            </td> <td class="tb">登记机关</td> <td class="">
                无锡市行政审批局
            </td> </tr> <tr> <td class="tb">所属地区</td> <td class="" style="max-width:301px;">
                江苏省
            </td> <td class="tb">英文名</td> <td class="">
                Jiangsu Hualan New Pharmaceutical Material Co., Ltd
            </td> </tr> <tr> <td class="tb">
                曾用名
            </td> <td class=""> <span>江阴兰陵瓶塞有限公司&nbsp;&nbsp;</span> </td> <td class="tb">
                参保人数
            </td> <td class="">
                372
            </td> </tr> <tr> <td class="tb">
                人员规模
            </td> <td class="">
                1000人以上
            </td> <td class="tb">
                营业期限
            </td> <td class="">
                1992-06-04 至 无固定期限
            </td> </tr> <tr> <td class="tb">企业地址</td> <td class="" colspan="3">
                 江阴市临港新城申港镇澄路1488号
                <a onclick="showMapModal('江阴市临港新城申港镇澄路1488号','')" class="m-l text-primary"> 查看地图</a> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()" class="m-l text-primary"> 附近企业</a> </td> </tr> <tr> <td class="tb">经营范围</td> <td class="" colspan="3">
                 生产橡胶瓶塞,塑料输液容器用聚丙烯组合盖、接口,低密度聚乙烯固体药用膜、袋;新型药用包装材料的技术开发、技术转让、技术咨询;国内贸易(不含限制及禁止类项目);自营和代理各类商品及技术的进出口业务,但国家限定企业经营或禁止进出口的商品和技术除外。(依法须经批准的项目,经相关部门批准后方可开展经营活动)             </td> </tr> </table> </section> <section id="partnern" class="panel b-a clearfix"> <div class="tcaption  m-t"> <h3 class="title">股东信息</h3> <span class="tbadge">38</span> <span class="watermark"></span> </div> <div id="partnerschart"> <div class="tcaption"> <h3 class="subtitle">工商股东统计分析</h3> <a class="hchart" onclick="hideChart(this)" href="javascript:;"> <span>收起</span> <i class="i i-arrow-up4"></i> </a> </div> <div class="float-wrap"> <div class="col-sm-6 col-xs-12 no-padding"><div id="partners-percent" class="nchart-item hmd"></div></div> <div class="col-sm-6 col-xs-12 no-padding" style="padding-left: 7px"><div id="partners-capi" class="nchart-item hmd"></div></div> </div> </div> <div class="clearfix m-t"></div> <div id="partnerslist"> <div class="tcaption"> <h3 class="subtitle">工商股东</h3> <span class="tbadge">38</span> </div> <div  style="position: relative;"> <div class="ntable-scrollcol"> <div style="width: 1200px;"> <table class="ntable ntable-odd npth"> <tbody> <tr> <th class="tx">序号</th> <th width=""><span class="m-r-sm">发起人及出资信息</span> <div class="npa gd"> <table class="ntable"> <tr> <th class="tx">序号</th> <th style="border-right: none;"><span class="m-r-sm">发起人及出资信息</span> <a onclick="showVipModal('最终受益人','成为VIP会员即可 查看历史工商变更、投资、股东、诉讼、受到的行政处罚等信息','zzsy','查看样例', '/firm_9cce0780ab7644008b73bc2120479d31.shtml#syrlistpos',true)">查看最终受益人></a> </th> </tr> </table> </div> <a onclick="showVipModal('最终受益人','成为VIP会员即可 查看历史工商变更、投资、股东、诉讼、受到的行政处罚等信息','zzsy','查看样例', '/firm_9cce0780ab7644008b73bc2120479d31.shtml#syrlistpos',true)">查看最终受益人></a> </th> <th>持股比例</th> <th>最终受益股份</th> <th>认缴出资额(万元)</th> <th>认缴出资日期</th> <th>实缴出资额(万元)</th> <th>实缴出资日期</th> <th>关联产品/机构</th> </tr> <tr> <td class="tx">
              
                1
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      1
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/bd51fff24d81b86140676e21b599e93a.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_bd51fff24d81b86140676e21b599e93a.html" target="_blank"><h3 class="seo font-14">
    江阴华兰机电科技有限公司</h3></a> <div class="m-t-xs ptag"> <span class="ntag sm text-success m-r-xs tooltip-br" data-trigger="hover" data-toggle="tooltip" data-placement="right" title="大股东是指股票占比较大的股东，它表示该股东与其余的股东相比较，它的占比最大。控股股东一定是大股东，但大股东却并不一定是控股股东。">大股东</span> </div> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('bd51fff24d81b86140676e21b599e93a','江阴华兰机电科技有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'江阴华兰机电科技有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/bd51fff24d81b86140676e21b599e93a.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_bd51fff24d81b86140676e21b599e93a.html" target="_blank"><h3 class="seo font-14">
    江阴华兰机电科技有限公司</h3></a> <div class="m-t-xs ptag"> <span class="ntag sm text-success m-r-xs tooltip-br" data-trigger="hover" data-toggle="tooltip" data-placement="right" title="大股东是指股票占比较大的股东，它表示该股东与其余的股东相比较，它的占比最大。控股股东一定是大股东，但大股东却并不一定是控股股东。">大股东</span> </div> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('bd51fff24d81b86140676e21b599e93a','江阴华兰机电科技有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'江阴华兰机电科技有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>40.71%</span> </td> <td width="100" class="text-center">
              42.249%
                            <div><a onclick="zhugeTrack('企业主页按钮点击',{'按钮名称':'股权链'});benefitDetail('bd51fff24d81b86140676e21b599e93a','大股东')">股权链></a></div> </td> <td class="text-center"> <span> 
                                                        3582.857
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  3582.857                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                2
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      2
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-5" first-letter="华"></span> </div> </td> <td> <a  href="/pl_p5748c03313a9627f6931d7a4248c06e.html"><h3 class="seo font-14">华一敏</h3></a> <div class="m-t-xs ptag"> <span class="ntag sm text-primary click" onclick="showVipModal('最终受益人','成为VIP会员即可 查看历史工商变更、投资、股东、诉讼、受到的行政处罚等信息','zzsy','查看样例', '/firm_9cce0780ab7644008b73bc2120479d31.shtml#syrlistpos',true)">最终受益人</span> </div> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'华一敏'});relatedList(1,'p5748c03313a9627f6931d7a4248c06e','华一敏')">他关联14家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-2" first-letter="华"></span> </div> </td> <td> <a  href="/pl_p5748c03313a9627f6931d7a4248c06e.html"><h3 class="seo font-14">华一敏</h3></a> <div class="m-t-xs ptag"> <span class="ntag sm text-primary click" onclick="showVipModal('最终受益人','成为VIP会员即可 查看历史工商变更、投资、股东、诉讼、受到的行政处罚等信息','zzsy','查看样例', '/firm_9cce0780ab7644008b73bc2120479d31.shtml#syrlistpos',true)">最终受益人</span> </div> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'华一敏'});relatedList(1,'p5748c03313a9627f6931d7a4248c06e','华一敏')">他关联14家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>25.00%</span> </td> <td width="100" class="text-center">
              33.4498%
                            <div><a onclick="zhugeTrack('企业主页按钮点击',{'按钮名称':'股权链'});benefitDetail('p5748c03313a9627f6931d7a4248c06e','最终受益人')">股权链></a></div> </td> <td class="text-center"> <span> 
                                                        2200
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2200                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                3
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      3
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/2afa54af1435e871bc11ecac6a2c764e.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_2afa54af1435e871bc11ecac6a2c764e.html" target="_blank"><h3 class="seo font-14">
    建银国际医疗保健投资管理（天津）有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('2afa54af1435e871bc11ecac6a2c764e','建银国际医疗保健投资管理（天津）有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'建银国际医疗保健投资管理（天津）有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/2afa54af1435e871bc11ecac6a2c764e.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_2afa54af1435e871bc11ecac6a2c764e.html" target="_blank"><h3 class="seo font-14">
    建银国际医疗保健投资管理（天津）有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('2afa54af1435e871bc11ecac6a2c764e','建银国际医疗保健投资管理（天津）有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'建银国际医疗保健投资管理（天津）有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>6.25%</span> </td> <td width="100" class="text-center">
              6.25%
                          </td> <td class="text-center"> <span> 
                                                        550
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  550                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center"> <a target="_blank" href="/investor_f016e59c7ad8b1d72903bb1aa5720d53.html">建银国际财富管理</a> </td> </tr> <tr> <td class="tx">
              
                4
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      4
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/c66d2d6d3f2e5543f2e2c96a94b37687.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_c66d2d6d3f2e5543f2e2c96a94b37687.html" target="_blank"><h3 class="seo font-14">
    苏州汾湖创业投资股份有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('c66d2d6d3f2e5543f2e2c96a94b37687','苏州汾湖创业投资股份有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'苏州汾湖创业投资股份有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/c66d2d6d3f2e5543f2e2c96a94b37687.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_c66d2d6d3f2e5543f2e2c96a94b37687.html" target="_blank"><h3 class="seo font-14">
    苏州汾湖创业投资股份有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('c66d2d6d3f2e5543f2e2c96a94b37687','苏州汾湖创业投资股份有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'苏州汾湖创业投资股份有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>4.00%</span> </td> <td width="100" class="text-center">
              4.00%
                          </td> <td class="text-center"> <span> 
                                                        352.0174
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  352.0174                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                5
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      5
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://co-image.qichacha.com/CompanyImage/6feb1eb7aa183d36f7ab89fefd407e00.jpg?x-oss-process=style/qcc_cmp"> </span> </td> <td> <a href="/firm_6feb1eb7aa183d36f7ab89fefd407e00.html" target="_blank"><h3 class="seo font-14">
    江苏康缘集团有限责任公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('6feb1eb7aa183d36f7ab89fefd407e00','江苏康缘集团有限责任公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'江苏康缘集团有限责任公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://co-image.qichacha.com/CompanyImage/6feb1eb7aa183d36f7ab89fefd407e00.jpg?x-oss-process=style/qcc_cmp"> </span> </td> <td> <a href="/firm_6feb1eb7aa183d36f7ab89fefd407e00.html" target="_blank"><h3 class="seo font-14">
    江苏康缘集团有限责任公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('6feb1eb7aa183d36f7ab89fefd407e00','江苏康缘集团有限责任公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'江苏康缘集团有限责任公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>3.43%</span> </td> <td width="100" class="text-center">
              3.43%
                          </td> <td class="text-center"> <span> 
                                                        302.1609
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  302.1609                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                6
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      6
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/3c14dc3d45e9416a07ce9af92aa6fc34.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_3c14dc3d45e9416a07ce9af92aa6fc34.html" target="_blank"><h3 class="seo font-14">
    江阴华恒投资管理有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('3c14dc3d45e9416a07ce9af92aa6fc34','江阴华恒投资管理有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'江阴华恒投资管理有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/3c14dc3d45e9416a07ce9af92aa6fc34.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_3c14dc3d45e9416a07ce9af92aa6fc34.html" target="_blank"><h3 class="seo font-14">
    江阴华恒投资管理有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('3c14dc3d45e9416a07ce9af92aa6fc34','江阴华恒投资管理有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'江阴华恒投资管理有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>1.84%</span> </td> <td width="100" class="text-center">
              1.84%
                          </td> <td class="text-center"> <span> 
                                                        162.1597
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  162.1597                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                7
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      7
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/0cf3e80f168626ac2d10ebde96ef59c8.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_0cf3e80f168626ac2d10ebde96ef59c8.html" target="_blank"><h3 class="seo font-14">
    江阴华平投资管理有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('0cf3e80f168626ac2d10ebde96ef59c8','江阴华平投资管理有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'江阴华平投资管理有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/0cf3e80f168626ac2d10ebde96ef59c8.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_0cf3e80f168626ac2d10ebde96ef59c8.html" target="_blank"><h3 class="seo font-14">
    江阴华平投资管理有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('0cf3e80f168626ac2d10ebde96ef59c8','江阴华平投资管理有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'江阴华平投资管理有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>1.71%</span> </td> <td width="100" class="text-center">
              1.71%
                          </td> <td class="text-center"> <span> 
                                                        150.0732
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  150.0732                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                8
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      8
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-2" first-letter="徐"></span> </div> </td> <td> <a  href="/pl_p9f47a69983d2a70e2051593c10c8d7e.html"><h3 class="seo font-14">徐中杰</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'徐中杰'});relatedList(1,'p9f47a69983d2a70e2051593c10c8d7e','徐中杰')">他关联18家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-5" first-letter="徐"></span> </div> </td> <td> <a  href="/pl_p9f47a69983d2a70e2051593c10c8d7e.html"><h3 class="seo font-14">徐中杰</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'徐中杰'});relatedList(1,'p9f47a69983d2a70e2051593c10c8d7e','徐中杰')">他关联18家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>1.60%</span> </td> <td width="100" class="text-center">
              1.60%
                          </td> <td class="text-center"> <span> 
                                                        141.0084
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  141.0084                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                9
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      9
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-10" first-letter="郭"></span> </div> </td> <td> <a  href="/pl_pf4e287811dfaddd203ee351ffcd8e2b.html"><h3 class="seo font-14">郭顺华</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'郭顺华'});relatedList(1,'pf4e287811dfaddd203ee351ffcd8e2b','郭顺华')">他关联13家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-8" first-letter="郭"></span> </div> </td> <td> <a  href="/pl_pf4e287811dfaddd203ee351ffcd8e2b.html"><h3 class="seo font-14">郭顺华</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'郭顺华'});relatedList(1,'pf4e287811dfaddd203ee351ffcd8e2b','郭顺华')">他关联13家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>1.60%</span> </td> <td width="100" class="text-center">
              1.60%
                          </td> <td class="text-center"> <span> 
                                                        141.0084
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  141.0084                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                10
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      10
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-1" first-letter="黄"></span> </div> </td> <td> <a  href="/pl_pbd8809988eaada153061b6c44b44d85.html"><h3 class="seo font-14">黄伟国</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'黄伟国'});relatedList(1,'pbd8809988eaada153061b6c44b44d85','黄伟国')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-2" first-letter="黄"></span> </div> </td> <td> <a  href="/pl_pbd8809988eaada153061b6c44b44d85.html"><h3 class="seo font-14">黄伟国</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'黄伟国'});relatedList(1,'pbd8809988eaada153061b6c44b44d85','黄伟国')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>1.53%</span> </td> <td width="100" class="text-center">
              1.53%
                          </td> <td class="text-center"> <span> 
                                                        134.9652
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  134.9652                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                11
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      11
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/3732e92d3deaadfb0a6ec0f45efe315a.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_3732e92d3deaadfb0a6ec0f45efe315a.html" target="_blank"><h3 class="seo font-14">
    泰州瑞洋立泰精化科技有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('3732e92d3deaadfb0a6ec0f45efe315a','泰州瑞洋立泰精化科技有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'泰州瑞洋立泰精化科技有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/3732e92d3deaadfb0a6ec0f45efe315a.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_3732e92d3deaadfb0a6ec0f45efe315a.html" target="_blank"><h3 class="seo font-14">
    泰州瑞洋立泰精化科技有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('3732e92d3deaadfb0a6ec0f45efe315a','泰州瑞洋立泰精化科技有限公司');zhugeTrack('企业主页-基本信息-股东信息-查看股权结构',{'股东名称':'泰州瑞洋立泰精化科技有限公司'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>1.14%</span> </td> <td width="100" class="text-center">
              1.14%
                          </td> <td class="text-center"> <span> 
                                                        100.7203
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  100.7203                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                12
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      12
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <img src="https://co-image.qichacha.com/PersonImage/p27093ec06e353427fa08a9db3dfcb9e.jpg"> </div> </td> <td> <a  href="/pl_p27093ec06e353427fa08a9db3dfcb9e.html"><h3 class="seo font-14">徐汉杰</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'徐汉杰'});relatedList(1,'p27093ec06e353427fa08a9db3dfcb9e','徐汉杰')">他关联77家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <img src="https://co-image.qichacha.com/PersonImage/p27093ec06e353427fa08a9db3dfcb9e.jpg"> </div> </td> <td> <a  href="/pl_p27093ec06e353427fa08a9db3dfcb9e.html"><h3 class="seo font-14">徐汉杰</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'徐汉杰'});relatedList(1,'p27093ec06e353427fa08a9db3dfcb9e','徐汉杰')">他关联77家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>1.03%</span> </td> <td width="100" class="text-center">
              1.03%
                          </td> <td class="text-center"> <span> 
                                                        90.6483
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  90.6483                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                13
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      13
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-2" first-letter="赵"></span> </div> </td> <td> <a  href="/pl_p428c82f04ba30464e461ed25a4f9d3b.html"><h3 class="seo font-14">赵怡新</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'赵怡新'});relatedList(1,'p428c82f04ba30464e461ed25a4f9d3b','赵怡新')">他关联4家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-3" first-letter="赵"></span> </div> </td> <td> <a  href="/pl_p428c82f04ba30464e461ed25a4f9d3b.html"><h3 class="seo font-14">赵怡新</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'赵怡新'});relatedList(1,'p428c82f04ba30464e461ed25a4f9d3b','赵怡新')">他关联4家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.97%</span> </td> <td width="100" class="text-center">
              0.97%
                          </td> <td class="text-center"> <span> 
                                                        85.6122
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  85.6122                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                14
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      14
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-2" first-letter="孙"></span> </div> </td> <td> <a  href="/pl_p0eee4d776af76d98e206fc0ac03dcea.html"><h3 class="seo font-14">孙炳荣</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'孙炳荣'});relatedList(1,'p0eee4d776af76d98e206fc0ac03dcea','孙炳荣')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-14" first-letter="孙"></span> </div> </td> <td> <a  href="/pl_p0eee4d776af76d98e206fc0ac03dcea.html"><h3 class="seo font-14">孙炳荣</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'孙炳荣'});relatedList(1,'p0eee4d776af76d98e206fc0ac03dcea','孙炳荣')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.92%</span> </td> <td width="100" class="text-center">
              0.92%
                          </td> <td class="text-center"> <span> 
                                                        80.5762
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  80.5762                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                15
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      15
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <img src="https://co-image.qichacha.com/PersonImage/p6f7ab4759dd2e497028ba4b56775919.jpg"> </div> </td> <td> <a  href="/pl_p6f7ab4759dd2e497028ba4b56775919.html"><h3 class="seo font-14">段小光</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'段小光'});relatedList(1,'p6f7ab4759dd2e497028ba4b56775919','段小光')">他关联40家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <img src="https://co-image.qichacha.com/PersonImage/p6f7ab4759dd2e497028ba4b56775919.jpg"> </div> </td> <td> <a  href="/pl_p6f7ab4759dd2e497028ba4b56775919.html"><h3 class="seo font-14">段小光</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'段小光'});relatedList(1,'p6f7ab4759dd2e497028ba4b56775919','段小光')">他关联40家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.81%</span> </td> <td width="100" class="text-center">
              0.81%
                          </td> <td class="text-center"> <span> 
                                                        71.5114
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  71.5114                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                16
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      16
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-5" first-letter="徐"></span> </div> </td> <td> <a  href="/pl_p3cc0d7eb1afec411b5e64bfea9cf0c2.html"><h3 class="seo font-14">徐志君</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'徐志君'});relatedList(1,'p3cc0d7eb1afec411b5e64bfea9cf0c2','徐志君')">他关联10家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-3" first-letter="徐"></span> </div> </td> <td> <a  href="/pl_p3cc0d7eb1afec411b5e64bfea9cf0c2.html"><h3 class="seo font-14">徐志君</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'徐志君'});relatedList(1,'p3cc0d7eb1afec411b5e64bfea9cf0c2','徐志君')">他关联10家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.80%</span> </td> <td width="100" class="text-center">
              0.80%
                          </td> <td class="text-center"> <span> 
                                                        70.5042
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  70.5042                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                17
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      17
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-3" first-letter="姚"></span> </div> </td> <td> <a  href="/pl_pa18f48637fb38a589fd3de7a91b3e3a.html"><h3 class="seo font-14">姚嘉</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'姚嘉'});relatedList(1,'pa18f48637fb38a589fd3de7a91b3e3a','姚嘉')">他关联6家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-4" first-letter="姚"></span> </div> </td> <td> <a  href="/pl_pa18f48637fb38a589fd3de7a91b3e3a.html"><h3 class="seo font-14">姚嘉</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'姚嘉'});relatedList(1,'pa18f48637fb38a589fd3de7a91b3e3a','姚嘉')">他关联6家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.74%</span> </td> <td width="100" class="text-center">
              0.74%
                          </td> <td class="text-center"> <span> 
                                                        65.4682
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  65.4682                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                18
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      18
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-11" first-letter="唐"></span> </div> </td> <td> <a  href="/pl_pdbb7562e928c58634ff16bf11474c44.html"><h3 class="seo font-14">唐保力</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'唐保力'});relatedList(1,'pdbb7562e928c58634ff16bf11474c44','唐保力')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-7" first-letter="唐"></span> </div> </td> <td> <a  href="/pl_pdbb7562e928c58634ff16bf11474c44.html"><h3 class="seo font-14">唐保力</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'唐保力'});relatedList(1,'pdbb7562e928c58634ff16bf11474c44','唐保力')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.74%</span> </td> <td width="100" class="text-center">
              0.74%
                          </td> <td class="text-center"> <span> 
                                                        65.4682
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  65.4682                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                19
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      19
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-5" first-letter="魏"></span> </div> </td> <td> <a  href="/pl_pd3be8995fb5c391c42ffc9084dc10cb.html"><h3 class="seo font-14">魏巍</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'魏巍'});relatedList(1,'pd3be8995fb5c391c42ffc9084dc10cb','魏巍')">他关联6家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-9" first-letter="魏"></span> </div> </td> <td> <a  href="/pl_pd3be8995fb5c391c42ffc9084dc10cb.html"><h3 class="seo font-14">魏巍</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'魏巍'});relatedList(1,'pd3be8995fb5c391c42ffc9084dc10cb','魏巍')">他关联6家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.57%</span> </td> <td width="100" class="text-center">
              0.57%
                          </td> <td class="text-center"> <span> 
                                                        50.3601
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  50.3601                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                20
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      20
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-14" first-letter="徐"></span> </div> </td> <td> <a  href="/pl_p35aedd6f24d20eb8f4babb5119e16b4.html"><h3 class="seo font-14">徐建兴</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'徐建兴'});relatedList(1,'p35aedd6f24d20eb8f4babb5119e16b4','徐建兴')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-8" first-letter="徐"></span> </div> </td> <td> <a  href="/pl_p35aedd6f24d20eb8f4babb5119e16b4.html"><h3 class="seo font-14">徐建兴</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'徐建兴'});relatedList(1,'p35aedd6f24d20eb8f4babb5119e16b4','徐建兴')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.46%</span> </td> <td width="100" class="text-center">
              0.46%
                          </td> <td class="text-center"> <span> 
                                                        40.2881
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  40.2881                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                21
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      21
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-11" first-letter="张"></span> </div> </td> <td> <a  href="/pl_p208b2e1256d06645a0672ba93afe4a0.html"><h3 class="seo font-14">张启方</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'张启方'});relatedList(1,'p208b2e1256d06645a0672ba93afe4a0','张启方')">他关联7家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-1" first-letter="张"></span> </div> </td> <td> <a  href="/pl_p208b2e1256d06645a0672ba93afe4a0.html"><h3 class="seo font-14">张启方</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'张启方'});relatedList(1,'p208b2e1256d06645a0672ba93afe4a0','张启方')">他关联7家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.40%</span> </td> <td width="100" class="text-center">
              0.40%
                          </td> <td class="text-center"> <span> 
                                                        35.2521
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  35.2521                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                22
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      22
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-4" first-letter="何"></span> </div> </td> <td> <a  href="/pl_p657d92bb60e174f5a73fba63df9764c.html"><h3 class="seo font-14">何文伟</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'何文伟'});relatedList(1,'p657d92bb60e174f5a73fba63df9764c','何文伟')">他关联5家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-6" first-letter="何"></span> </div> </td> <td> <a  href="/pl_p657d92bb60e174f5a73fba63df9764c.html"><h3 class="seo font-14">何文伟</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'何文伟'});relatedList(1,'p657d92bb60e174f5a73fba63df9764c','何文伟')">他关联5家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.40%</span> </td> <td width="100" class="text-center">
              0.40%
                          </td> <td class="text-center"> <span> 
                                                        35.2521
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  35.2521                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                23
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      23
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-9" first-letter="黄"></span> </div> </td> <td> <a  href="/pl_p9aa63dbcee79bbcbe102774e0ca892d.html"><h3 class="seo font-14">黄翠娟</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'黄翠娟'});relatedList(1,'p9aa63dbcee79bbcbe102774e0ca892d','黄翠娟')">他关联17家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-4" first-letter="黄"></span> </div> </td> <td> <a  href="/pl_p9aa63dbcee79bbcbe102774e0ca892d.html"><h3 class="seo font-14">黄翠娟</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'黄翠娟'});relatedList(1,'p9aa63dbcee79bbcbe102774e0ca892d','黄翠娟')">他关联17家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.40%</span> </td> <td width="100" class="text-center">
              0.40%
                          </td> <td class="text-center"> <span> 
                                                        35.2521
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  35.2521                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                24
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      24
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-14" first-letter="刘"></span> </div> </td> <td> <a  href="/pl_p119fcdaa9e17e311be0f58cc8058fb3.html"><h3 class="seo font-14">刘红卫</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'刘红卫'});relatedList(1,'p119fcdaa9e17e311be0f58cc8058fb3','刘红卫')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-2" first-letter="刘"></span> </div> </td> <td> <a  href="/pl_p119fcdaa9e17e311be0f58cc8058fb3.html"><h3 class="seo font-14">刘红卫</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'刘红卫'});relatedList(1,'p119fcdaa9e17e311be0f58cc8058fb3','刘红卫')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.34%</span> </td> <td width="100" class="text-center">
              0.34%
                          </td> <td class="text-center"> <span> 
                                                        30.2161
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  30.2161                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                25
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      25
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-5" first-letter="李"></span> </div> </td> <td> <a  href="/pl_p86d1a4ba07b23530aa5bf35d7c8f3b4.html"><h3 class="seo font-14">李秀</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'李秀'});relatedList(1,'p86d1a4ba07b23530aa5bf35d7c8f3b4','李秀')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-4" first-letter="李"></span> </div> </td> <td> <a  href="/pl_p86d1a4ba07b23530aa5bf35d7c8f3b4.html"><h3 class="seo font-14">李秀</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'李秀'});relatedList(1,'p86d1a4ba07b23530aa5bf35d7c8f3b4','李秀')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.34%</span> </td> <td width="100" class="text-center">
              0.34%
                          </td> <td class="text-center"> <span> 
                                                        30.2161
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  30.2161                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                26
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      26
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-3" first-letter="高"></span> </div> </td> <td> <a  href="/pl_p73c2a4d9e1560be87f939f6d74fae4d.html"><h3 class="seo font-14">高集馥</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'高集馥'});relatedList(1,'p73c2a4d9e1560be87f939f6d74fae4d','高集馥')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-7" first-letter="高"></span> </div> </td> <td> <a  href="/pl_p73c2a4d9e1560be87f939f6d74fae4d.html"><h3 class="seo font-14">高集馥</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'高集馥'});relatedList(1,'p73c2a4d9e1560be87f939f6d74fae4d','高集馥')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.32%</span> </td> <td width="100" class="text-center">
              0.32%
                          </td> <td class="text-center"> <span> 
                                                        28.2017
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  28.2017                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                27
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      27
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-9" first-letter="朱"></span> </div> </td> <td> <a  href="/pl_p0ac85ba23e4e4d9ab40ac9cc47b5603.html"><h3 class="seo font-14">朱明</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'朱明'});relatedList(1,'p0ac85ba23e4e4d9ab40ac9cc47b5603','朱明')">他关联2家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-13" first-letter="朱"></span> </div> </td> <td> <a  href="/pl_p0ac85ba23e4e4d9ab40ac9cc47b5603.html"><h3 class="seo font-14">朱明</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'朱明'});relatedList(1,'p0ac85ba23e4e4d9ab40ac9cc47b5603','朱明')">他关联2家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.19%</span> </td> <td width="100" class="text-center">
              0.19%
                          </td> <td class="text-center"> <span> 
                                                        17.1224
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  17.1224                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                28
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      28
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-14" first-letter="杨"></span> </div> </td> <td> <a  href="/pl_p252fd81e01748dedfcd92b219584cd5.html"><h3 class="seo font-14">杨瑞芬</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'杨瑞芬'});relatedList(1,'p252fd81e01748dedfcd92b219584cd5','杨瑞芬')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-9" first-letter="杨"></span> </div> </td> <td> <a  href="/pl_p252fd81e01748dedfcd92b219584cd5.html"><h3 class="seo font-14">杨瑞芬</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'杨瑞芬'});relatedList(1,'p252fd81e01748dedfcd92b219584cd5','杨瑞芬')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.19%</span> </td> <td width="100" class="text-center">
              0.19%
                          </td> <td class="text-center"> <span> 
                                                        17.1224
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  17.1224                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                29
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      29
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-14" first-letter="陈"></span> </div> </td> <td> <a  href="/pl_p9d5feacf1b29f647d26dd5b80a24466.html"><h3 class="seo font-14">陈琴芬</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'陈琴芬'});relatedList(1,'p9d5feacf1b29f647d26dd5b80a24466','陈琴芬')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-2" first-letter="陈"></span> </div> </td> <td> <a  href="/pl_p9d5feacf1b29f647d26dd5b80a24466.html"><h3 class="seo font-14">陈琴芬</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'陈琴芬'});relatedList(1,'p9d5feacf1b29f647d26dd5b80a24466','陈琴芬')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.19%</span> </td> <td width="100" class="text-center">
              0.19%
                          </td> <td class="text-center"> <span> 
                                                        17.1224
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  17.1224                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                30
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      30
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-11" first-letter="殷"></span> </div> </td> <td> <a  href="/pl_pc430b08e72f9006cbdda9331f4cf3c5.html"><h3 class="seo font-14">殷洪林</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'殷洪林'});relatedList(1,'pc430b08e72f9006cbdda9331f4cf3c5','殷洪林')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-2" first-letter="殷"></span> </div> </td> <td> <a  href="/pl_pc430b08e72f9006cbdda9331f4cf3c5.html"><h3 class="seo font-14">殷洪林</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'殷洪林'});relatedList(1,'pc430b08e72f9006cbdda9331f4cf3c5','殷洪林')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.19%</span> </td> <td width="100" class="text-center">
              0.19%
                          </td> <td class="text-center"> <span> 
                                                        17.1224
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  17.1224                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                31
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      31
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-2" first-letter="王"></span> </div> </td> <td> <a  href="/pl_p91ad9d336c1521a7e3e851100031eaa.html"><h3 class="seo font-14">王玉珠</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'王玉珠'});relatedList(1,'p91ad9d336c1521a7e3e851100031eaa','王玉珠')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-2" first-letter="王"></span> </div> </td> <td> <a  href="/pl_p91ad9d336c1521a7e3e851100031eaa.html"><h3 class="seo font-14">王玉珠</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'王玉珠'});relatedList(1,'p91ad9d336c1521a7e3e851100031eaa','王玉珠')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.17%</span> </td> <td width="100" class="text-center">
              0.17%
                          </td> <td class="text-center"> <span> 
                                                        15.108
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  15.108                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                32
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      32
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-4" first-letter="黄"></span> </div> </td> <td> <a  href="/pl_p95360910802739414ed7fa9f0925e0f.html"><h3 class="seo font-14">黄阿焕</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'黄阿焕'});relatedList(1,'p95360910802739414ed7fa9f0925e0f','黄阿焕')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-4" first-letter="黄"></span> </div> </td> <td> <a  href="/pl_p95360910802739414ed7fa9f0925e0f.html"><h3 class="seo font-14">黄阿焕</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'黄阿焕'});relatedList(1,'p95360910802739414ed7fa9f0925e0f','黄阿焕')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.16%</span> </td> <td width="100" class="text-center">
              0.16%
                          </td> <td class="text-center"> <span> 
                                                        14.1008
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  14.1008                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                33
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      33
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-5" first-letter="殷"></span> </div> </td> <td> <a  href="/pl_pd8e32622f52f1899c01d248ef35b5b1.html"><h3 class="seo font-14">殷蓉辉</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'殷蓉辉'});relatedList(1,'pd8e32622f52f1899c01d248ef35b5b1','殷蓉辉')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-1" first-letter="殷"></span> </div> </td> <td> <a  href="/pl_pd8e32622f52f1899c01d248ef35b5b1.html"><h3 class="seo font-14">殷蓉辉</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'殷蓉辉'});relatedList(1,'pd8e32622f52f1899c01d248ef35b5b1','殷蓉辉')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.16%</span> </td> <td width="100" class="text-center">
              0.16%
                          </td> <td class="text-center"> <span> 
                                                        14.1008
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  14.1008                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                34
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      34
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-11" first-letter="孟"></span> </div> </td> <td> <a  href="/pl_pe4796b4750435050e60b8d9f5f298fd.html"><h3 class="seo font-14">孟昱</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'孟昱'});relatedList(1,'pe4796b4750435050e60b8d9f5f298fd','孟昱')">他关联5家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-9" first-letter="孟"></span> </div> </td> <td> <a  href="/pl_pe4796b4750435050e60b8d9f5f298fd.html"><h3 class="seo font-14">孟昱</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'孟昱'});relatedList(1,'pe4796b4750435050e60b8d9f5f298fd','孟昱')">他关联5家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.16%</span> </td> <td width="100" class="text-center">
              0.16%
                          </td> <td class="text-center"> <span> 
                                                        14.1008
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  14.1008                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                35
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      35
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-10" first-letter="李"></span> </div> </td> <td> <a  href="/pl_p516d6e59c0babdd55d8526356102ead.html"><h3 class="seo font-14">李娟</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'李娟'});relatedList(1,'p516d6e59c0babdd55d8526356102ead','李娟')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-10" first-letter="李"></span> </div> </td> <td> <a  href="/pl_p516d6e59c0babdd55d8526356102ead.html"><h3 class="seo font-14">李娟</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'李娟'});relatedList(1,'p516d6e59c0babdd55d8526356102ead','李娟')">他关联3家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.14%</span> </td> <td width="100" class="text-center">
              0.14%
                          </td> <td class="text-center"> <span> 
                                                        12.0864
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  12.0864                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                36
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      36
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-3" first-letter="许"></span> </div> </td> <td> <a  href="/pl_p904ea083f2bae72a2b5e2df256e90ba.html"><h3 class="seo font-14">许一花</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'许一花'});relatedList(1,'p904ea083f2bae72a2b5e2df256e90ba','许一花')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-6" first-letter="许"></span> </div> </td> <td> <a  href="/pl_p904ea083f2bae72a2b5e2df256e90ba.html"><h3 class="seo font-14">许一花</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'许一花'});relatedList(1,'p904ea083f2bae72a2b5e2df256e90ba','许一花')">他关联1家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.11%</span> </td> <td width="100" class="text-center">
              0.11%
                          </td> <td class="text-center"> <span> 
                                                        10.072
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  10.072                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                37
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      37
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-11" first-letter="朱"></span> </div> </td> <td> <a  href="/pl_pca5e2cea8eb6417432aa1e79dce7401.html"><h3 class="seo font-14">朱凯</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'朱凯'});relatedList(1,'pca5e2cea8eb6417432aa1e79dce7401','朱凯')">他关联2家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-7" first-letter="朱"></span> </div> </td> <td> <a  href="/pl_pca5e2cea8eb6417432aa1e79dce7401.html"><h3 class="seo font-14">朱凯</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'朱凯'});relatedList(1,'pca5e2cea8eb6417432aa1e79dce7401','朱凯')">他关联2家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.11%</span> </td> <td width="100" class="text-center">
              0.11%
                          </td> <td class="text-center"> <span> 
                                                        10.072
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  10.072                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> <tr> <td class="tx">
              
                38
                
             </td> <td width="332"> <div class="npa ntd gd"> <table class="ntable"> <tr> <td class="tx">
                      38
                    </td> <td style="padding-left: 11px;"> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-12" first-letter="卜"></span> </div> </td> <td> <a  href="/pl_pd8cd500e5f73487fa0988000c1367b4.html"><h3 class="seo font-14">卜忠兴</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'卜忠兴'});relatedList(1,'pd8cd500e5f73487fa0988000c1367b4','卜忠兴')">他关联5家企业 > </a> </div> </td> </tr> </table> </td> </tr> </table> </div> <table class="insert-table"> <tr> <td width="50"> <div class="headimg"> <span class="usericon headn color-5" first-letter="卜"></span> </div> </td> <td> <a  href="/pl_pd8cd500e5f73487fa0988000c1367b4.html"><h3 class="seo font-14">卜忠兴</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="zhugeTrack('关联企业按钮点击',{'按钮位置':'股东信息','关联目标':'卜忠兴'});relatedList(1,'pd8cd500e5f73487fa0988000c1367b4','卜忠兴')">他关联5家企业 > </a> </div> </td> </tr> </table> </td> <td class="text-center"> <span>0.11%</span> </td> <td width="100" class="text-center">
              0.11%
                          </td> <td class="text-center"> <span> 
                                                        10.072
                                        <br/> </span> </td> <td class="text-center"> <span> 
                 
                  2009-10-15                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  10.072                    <br/> </span> </td> <td class="text-center"> <span>
                   
                 
                  2009-10-15                    <br/> </span> </td> <td width="160" class="text-center">
                                    -
                            </td> </tr> </tbody> </table> </div> </div> </div> <script type="text/javascript">
  $(function(){
      setMouseWheelV('#partnerslist .ntable-scrollcol');
      $.each($('#partnerslist td .npa'),function(i,dom) {
        if($(dom).parent().height()>0){
          $(dom).parent().css('vertical-align','top');
          $(dom).removeClass('ntd');
          $(dom).height($(dom).parent().height()+23);
        }
      })
    })
</script> <div> </div> <script type="text/javascript">
  $('#partnerslist [data-toggle="tooltip"]').tooltip();
  var optionArr = ['partnerscapi','partnersratio'];
  var descArr = ['认缴金额','持股比例'];
  var hiddenName = '';
  var hiddenValue = '';
  var hiddenDesc = '';
  for(var i=0;i<optionArr.length;i++){
      hiddenName = optionArr[i];
      hiddenValue = $("input[name=" + hiddenName + "]").val();
      hiddenDesc = $("input[name=" + hiddenName + "]").attr('data-desc');
      var text = '.' + hiddenName;
      if(hiddenValue != '' && hiddenValue != '0'){
          $(text).text(hiddenDesc);
      }else{
          $(text).text(descArr[i]);
      }
  }
  $(function () {
      $('#partnerslist .chooseBase').find('a').on('click',function(){
          var targetDiv = $(this).parent().parent().parent().parent();
          var target = targetDiv.attr('data-box');
          var optionArr = [];
          var hiddenName = '';
          var hiddenValue = '';
          var ajaxData = {};
          var optionArr = ['partnerscapi','partnersratio','capiUnit'];
          var option = $(this).attr('data-option');
          option = target + option;
          var value = $(this).attr('data-value');
          var text = $(this).text();
          var textArr = text.split('(');
          $("input[name=" + option + "]").val(value);
          $("input[name=" + option + "]").attr('data-desc',textArr[0]);
          //取所有筛选条件的值
          for(var i=0;i<optionArr.length;i++){
              hiddenName = optionArr[i];
              hiddenValue = $("input[name=" + hiddenName + "]").val();
              ajaxData[hiddenName] = hiddenValue;
          }
          //拼接其他参数
          ajaxData['unique'] = $("#unique").val();
          ajaxData['companyname'] = $("#companyname").val();
          ajaxData['tab'] = 'base';
          ajaxData['box'] = 'partners';
          ajaxData['p'] = '1';
          getTabListNew(ajaxData);
      });
  });
</script> </div> </section> <section class="panel b-a clear guquan-section" id="guquan"> <div class="tcaption"> <h3 class="title">股权穿透图</h3> <span class="watermark"></span> </div> <table class="ntable"> <tr> <th style="text-align: left;position: relative;">
                江苏华兰药用新材料股份有限公司
                <div id="guquanIframeTool" class="guquan-tool"> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()" target="_blank"><span class="screen">&nbsp;</span><span>全屏查看</span></a> <a class="m-l" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()"><span class="save">&nbsp;</span><span>下载图谱</span></a> </div> </th> </tr> <tr> <td style="padding: 0px;"> <iframe id="guquanIframe" scrolling="no" src="company_guquan?keyNo=5f981c1538705fe2ec4891565b370edc&iframe=1" frameborder="0"></iframe> </td> </tr> </table> </section> <section class="panel b-a clear" id="Mainmember"> <div class="tcaption"> <h3 class="title"> 主要人员</h3> <span class="tbadge">12</span> <span class="watermark"></span> </div> <table class="ntable ntable-odd"> <tr> <th class=""> 序号</th> <th class=""> 姓名</th> <th class="">职务</th> </tr> <tr> <td class="tx">1</td> <td width="50%"> <span class="usericon headn color-10" first-letter="华"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_ped4659e89d457c7f2a22fa1fac34c98.html" class="c_a" title="华国平"><h3 class="seo font-14">华国平</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 6 家企业 > </a> </div> </td> <td  class="text-center">
                董事长
            </td> </tr> <tr> <td class="tx">2</td> <td width="50%"> <span class="usericon headn color-12" first-letter="华"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_p5748c03313a9627f6931d7a4248c06e.html" class="c_a" title="华一敏"><h3 class="seo font-14">华一敏</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 14 家企业 > </a> </div> </td> <td  class="text-center">
                总经理,董事
            </td> </tr> <tr> <td class="tx">3</td> <td width="50%"> <span class="usericon headn color-7" first-letter="虞"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_p2d9f9c5b89aaa2c0ee5468e30075c1a.html" class="c_a" title="虞丽新"><h3 class="seo font-14">虞丽新</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 4 家企业 > </a> </div> </td> <td  class="text-center">
                董事
            </td> </tr> <tr> <td class="tx">4</td> <td width="50%"> <span class="usericon headn color-1" first-letter="肖"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_pe0c0198c583eeb5bd0d76780144d7d8.html" class="c_a" title="肖锋"><h3 class="seo font-14">肖锋</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 1 家企业 > </a> </div> </td> <td  class="text-center">
                董事
            </td> </tr> <tr> <td class="tx">5</td> <td width="50%"> <span class="usericon headn color-1" first-letter="李"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_p77b214a04c4a814a26df0443ac6f6c0.html" class="c_a" title="李论"><h3 class="seo font-14">李论</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 4 家企业 > </a> </div> </td> <td  class="text-center">
                董事
            </td> </tr> <tr> <td class="tx">6</td> <td width="50%"> <span class="usericon headn color-9" first-letter="柳"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_pr466867135e1adaf8a356f7e09b6ea3.html" class="c_a" title="柳丹"><h3 class="seo font-14">柳丹</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 1 家企业 > </a> </div> </td> <td  class="text-center">
                董事
            </td> </tr> <tr> <td class="tx">7</td> <td width="50%"> <span class="usericon headn color-8" first-letter="王"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_pa1790888462c5a72285908248c95605.html" class="c_a" title="王兆千"><h3 class="seo font-14">王兆千</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 3 家企业 > </a> </div> </td> <td  class="text-center">
                董事
            </td> </tr> <tr> <td class="tx">8</td> <td width="50%"> <span class="usericon headn color-9" first-letter="马"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_paf3eb88d9ed459de1b68a3db7c2f66b.html" class="c_a" title="马卫国"><h3 class="seo font-14">马卫国</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 17 家企业 > </a> </div> </td> <td  class="text-center">
                董事
            </td> </tr> <tr> <td class="tx">9</td> <td width="50%"> <span class="usericon headn color-7" first-letter="裘"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_p3672f2f37298c9657b448dc797bcb67.html" class="c_a" title="裘索"><h3 class="seo font-14">裘索</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 12 家企业 > </a> </div> </td> <td  class="text-center">
                董事
            </td> </tr> <tr> <td class="tx">10</td> <td width="50%"> <span class="usericon headn color-8" first-letter="陈"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_pr48ee38d8287c20fb69ebbebdba0f8d.html" class="c_a" title="陈禹"><h3 class="seo font-14">陈禹</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 1 家企业 > </a> </div> </td> <td  class="text-center">
                监事
            </td> </tr> <tr> <td class="tx">11</td> <td width="50%"> <span class="usericon headn color-4" first-letter="叶"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_pr13e8a914fdfe54b7fa06eb90e85579.html" class="c_a" title="叶玉萍"><h3 class="seo font-14">叶玉萍</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 1 家企业 > </a> </div> </td> <td  class="text-center">
                监事
            </td> </tr> <tr> <td class="tx">12</td> <td width="50%"> <span class="usericon headn color-7" first-letter="刘"></span> <div class="whead-text" style="width: 365px;"> <a href="/pl_p98390e37c07897061a013b176ef433d.html" class="c_a" title="刘利剑"><h3 class="seo font-14">刘利剑</h3></a> <a class="btn-touzi pull-right" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">他关联 6 家企业 > </a> </div> </td> <td  class="text-center">
                其他人员
            </td> </tr> </table> </section> <section class="panel b-a clear"> <div class="tcaption  m-t"> <h3 class="title">对外投资统计分析</h3> <a class="hchart" onclick="hideChart(this)" href="javascript:;"> <span>收起</span> <i class="i i-arrow-up4"></i> </a> </div> <div class="float-wrap"> <div class="col-sm-6 col-xs-12 no-padding"><div id="touzi-province" class="nchart-item hmd"></div></div> <div class="col-sm-6 col-xs-12 no-padding" style="padding-left: 7px"><div id="touzi-industry" class="nchart-item hmd"></div></div> </div> </section> <section class="panel b-a" id="touzilist"> <div class="tcaption"> <span class="title"> 对外投资</span> <span class="tbadge">6</span> <span class="thist">（查看更多1条 <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">历史对外投资</a>）</span> <div class="chooseBase" data-box="touzi" style="float: right"> </div> <span class="watermark"></span> </div> <table class="ntable ntable-odd npth"> <tbody> <tr> <th class="tx">序号</th> <th class="">被投资企业名称</th> <th class="">法定代表人</th> <th class="">注册资本</th> <th class="">投资比例</th> <th class="">投资数额</th> <th class="">成立日期</th> <th>状态</th> </tr> <tr> <td class="text-center">1</td> <td width=""> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/b616a91319b1dd8dd62a7209fdbe6eed.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_b616a91319b1dd8dd62a7209fdbe6eed.html" target="_blank" ><h3 class="seo font-14">重庆市涪陵三海兰陵有限责任公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('b616a91319b1dd8dd62a7209fdbe6eed','重庆市涪陵三海兰陵有限责任公司');zhugeTrack('企业主页按钮点击',{'按钮名称':'股权结构'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td width="150"> <table class="insert-table"> <tr> <td> <a href="/pl_p5748c03313a9627f6931d7a4248c06e.html"><h3 class="seo font-14">华一敏</h3></a> <div class="m-t-xs"> <a class="btn-touzi pull-left" onclick="relatedList(1,'p5748c03313a9627f6931d7a4248c06e','华一敏');zhugeTrack('关联企业按钮点击',{'按钮位置':'对外投资','关联目标':'华一敏'});">他关联14家企业 > </a> </div> </td> </tr> </table> </td> <td  width="110" class="text-center">

                      2858万元人民币 
                    </td> <td width="90" class="text-center">
                        100%
                    </td> <td  width="110" class="text-center"> <span>
                           2858万元人民币 
                        </span> </td> <td width="103" class="text-center">
                       1998-07-15                    </td> <td width="80" class="text-center"> <span class="text-success">存续</span> </td> </tr> <tr> <td class="text-center">2</td> <td width=""> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/047a1350764f17f85ebabcfc5860b133.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_047a1350764f17f85ebabcfc5860b133.html" target="_blank" ><h3 class="seo font-14">重庆渡澄贸易有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('047a1350764f17f85ebabcfc5860b133','重庆渡澄贸易有限公司');zhugeTrack('企业主页按钮点击',{'按钮名称':'股权结构'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td width="150"> <table class="insert-table"> <tr> <td> <a href="/pl_p5748c03313a9627f6931d7a4248c06e.html"><h3 class="seo font-14">华一敏</h3></a> <div class="m-t-xs"> <a class="btn-touzi pull-left" onclick="relatedList(1,'p5748c03313a9627f6931d7a4248c06e','华一敏');zhugeTrack('关联企业按钮点击',{'按钮位置':'对外投资','关联目标':'华一敏'});">他关联14家企业 > </a> </div> </td> </tr> </table> </td> <td  width="110" class="text-center">

                      2000万元人民币 
                    </td> <td width="90" class="text-center">
                        100%
                    </td> <td  width="110" class="text-center"> <span>
                           2000万元人民币 
                        </span> </td> <td width="103" class="text-center">
                       2016-08-05                    </td> <td width="80" class="text-center"> <span class="text-success">存续</span> </td> </tr> <tr> <td class="text-center">3</td> <td width=""> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/272ec4f22c5de9dd43bfe073d51cfebd.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_272ec4f22c5de9dd43bfe073d51cfebd.html" target="_blank" ><h3 class="seo font-14">江苏华杨医疗科技有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('272ec4f22c5de9dd43bfe073d51cfebd','江苏华杨医疗科技有限公司');zhugeTrack('企业主页按钮点击',{'按钮名称':'股权结构'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td width="150"> <table class="insert-table"> <tr> <td> <a href="/pl_p5748c03313a9627f6931d7a4248c06e.html"><h3 class="seo font-14">华一敏</h3></a> <div class="m-t-xs"> <a class="btn-touzi pull-left" onclick="relatedList(1,'p5748c03313a9627f6931d7a4248c06e','华一敏');zhugeTrack('关联企业按钮点击',{'按钮位置':'对外投资','关联目标':'华一敏'});">他关联14家企业 > </a> </div> </td> </tr> </table> </td> <td  width="110" class="text-center">

                      2000万元人民币 
                    </td> <td width="90" class="text-center">
                        100%
                    </td> <td  width="110" class="text-center"> <span>
                           2000万元人民币 
                        </span> </td> <td width="103" class="text-center">
                       2006-05-23                    </td> <td width="80" class="text-center"> <span class="text-success">存续</span> </td> </tr> <tr> <td class="text-center">4</td> <td width=""> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/786f4f9c8628abdd4557a9c3cfaac932.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_786f4f9c8628abdd4557a9c3cfaac932.html" target="_blank" ><h3 class="seo font-14">重庆华兰商贸有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('786f4f9c8628abdd4557a9c3cfaac932','重庆华兰商贸有限公司');zhugeTrack('企业主页按钮点击',{'按钮名称':'股权结构'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td width="150"> <table class="insert-table"> <tr> <td> <a href="/pl_p334f7e80c61ded944ef16ce53532073.html"><h3 class="seo font-14">杨菊兰</h3></a> <div class="m-t-xs"> <a class="btn-touzi pull-left" onclick="relatedList(1,'p334f7e80c61ded944ef16ce53532073','杨菊兰');zhugeTrack('关联企业按钮点击',{'按钮位置':'对外投资','关联目标':'杨菊兰'});">他关联6家企业 > </a> </div> </td> </tr> </table> </td> <td  width="110" class="text-center">

                      2000万元人民币 
                    </td> <td width="90" class="text-center">
                        100%
                    </td> <td  width="110" class="text-center"> <span>
                           2000万元人民币 
                        </span> </td> <td width="103" class="text-center">
                       2012-09-03                    </td> <td width="80" class="text-center"> <span class="text-danger">注销</span> </td> </tr> <tr> <td class="text-center">5</td> <td width=""> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/c2d9469e8d81052fe8f44028a35f68aa.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_c2d9469e8d81052fe8f44028a35f68aa.html" target="_blank" ><h3 class="seo font-14">泰州华兰药用新材料有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('c2d9469e8d81052fe8f44028a35f68aa','泰州华兰药用新材料有限公司');zhugeTrack('企业主页按钮点击',{'按钮名称':'股权结构'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td width="150"> <table class="insert-table"> <tr> <td> <a href="/pl_pfb2a6ea967c5fd6d2ddacbc80601e7a.html"><h3 class="seo font-14">严治国</h3></a> <div class="m-t-xs"> <a class="btn-touzi pull-left" onclick="relatedList(1,'pfb2a6ea967c5fd6d2ddacbc80601e7a','严治国');zhugeTrack('关联企业按钮点击',{'按钮位置':'对外投资','关联目标':'严治国'});">他关联2家企业 > </a> </div> </td> </tr> </table> </td> <td  width="110" class="text-center">

                      100万元人民币 
                    </td> <td width="90" class="text-center">
                        100%
                    </td> <td  width="110" class="text-center"> <span>
                           100万元人民币 
                        </span> </td> <td width="103" class="text-center">
                       2014-08-14                    </td> <td width="80" class="text-center"> <span class="text-danger">注销</span> </td> </tr> <tr> <td class="text-center">6</td> <td width=""> <table class="insert-table"> <tr> <td width="50"> <span class="headimg"> <img src="https://qccdata.qichacha.com/AutoImage/e9930e3cc5de38b1867aca9a8fe43668.jpg?x-oss-process=image/resize,w_120"> </span> </td> <td> <a href="/firm_e9930e3cc5de38b1867aca9a8fe43668.html" target="_blank" ><h3 class="seo font-14">江阴兰陵医药包装科技有限公司</h3></a> <div class="clearfix m-t-xs"> <a class="btn-touzi pull-left" onclick="guquanList2('e9930e3cc5de38b1867aca9a8fe43668','江阴兰陵医药包装科技有限公司');zhugeTrack('企业主页按钮点击',{'按钮名称':'股权结构'});">股权结构 > </a> </div> </td> </tr> </table> </td> <td width="150"> <table class="insert-table"> <tr> <td> <a href="/pl_ped4659e89d457c7f2a22fa1fac34c98.html"><h3 class="seo font-14">华国平</h3></a> <div class="m-t-xs"> <a class="btn-touzi pull-left" onclick="relatedList(1,'ped4659e89d457c7f2a22fa1fac34c98','华国平');zhugeTrack('关联企业按钮点击',{'按钮位置':'对外投资','关联目标':'华国平'});">他关联6家企业 > </a> </div> </td> </tr> </table> </td> <td  width="110" class="text-center">

                      250万美元 
                    </td> <td width="90" class="text-center">
                        51.00%
                    </td> <td  width="110" class="text-center"> <span>
                           127.5万美元 
                        </span> </td> <td width="103" class="text-center">
                       2008-11-19                    </td> <td width="80" class="text-center"> <span class="text-danger">注销</span> </td> </tr> </tbody> </table> <div> <nav class="text-right">
    亲，<a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()" class="text-primary">登录</a>后可以查看更多数据哦
</nav> </div> <script type="text/javascript">
        var optionArr = ['touzistatus','touziratio','touzicapi'];
        var descArr = ['全部状态','投资比例','注册资本'];
        var hiddenName = '';
        var hiddenValue = '';
        var hiddenDesc = '';
        for(var i=0;i<optionArr.length;i++){
            hiddenName = optionArr[i];
            hiddenValue = $("input[name=" + hiddenName + "]").val();
            hiddenDesc = $("input[name=" + hiddenName + "]").attr('data-desc');
            var text = '.' + hiddenName;
            if(hiddenValue != '' && hiddenValue != '0'){
                $(text).text(hiddenDesc);
            }else{
                $(text).text(descArr[i]);
            }
        }
        $(function () {
            $('#touzilist .chooseBase').find('a').on('click',function(){
                var targetDiv = $(this).parent().parent().parent().parent();
                var target = targetDiv.attr('data-box');
                var optionArr = [];
                var hiddenName = '';
                var hiddenValue = '';
                var ajaxData = {};
                switch(target){
                    case 'touzi':
                        optionArr = ['touzistatus','touziratio','touzicapi'];
                        ajaxData['box'] = 'touzi';
                        break;
                    default :
                        break;
                }
                var option = $(this).attr('data-option');
                option = target + option;
                var value = $(this).attr('data-value');
                var text = $(this).text();
                var textArr = text.split('(');
                $("input[name=" + option + "]").val(value);
                $("input[name=" + option + "]").attr('data-desc',textArr[0]);
                //取所有筛选条件的值
                for(var i=0;i<optionArr.length;i++){
                    hiddenName = optionArr[i];
                    hiddenValue = $("input[name=" + hiddenName + "]").val();
                    ajaxData[hiddenName] = hiddenValue;
                }
                //拼接其他参数
                ajaxData['unique'] = $("#unique").val();
                ajaxData['companyname'] = $("#companyname").val();
                ajaxData['tab'] = 'base';
                ajaxData['p'] = '1';
                getTabListNew(ajaxData);
            });
        });
    </script> </section> <section class="panel b-a" id="Comintroduce"> <div class="tcaption"> <h3 class="title">公司简介</h3> <span class="watermark"></span> </div> <div class="" style="width:100%;margin: 0 auto;"> <div style="border:#E6E6E6 1px solid;padding: 15px;">
             企 业 简 介
江苏华兰药用新材料股份有限公司（原江阴兰陵瓶塞有限公司）位于江苏省江阴市临港新城申港镇澄路1488号，成立于1992年，经过二十年的不懈努力，现已发展成为一家实力雄厚、品种齐全、技术领先、规模优势显着的专业生产直接或间接接触药物包装材料的现代化高新技术企业。2010年实现销售收入57771万元，利税6379万元。连续叁年列入江阴百强企业。2009年公司被纳入2009中国医疗健康产业最具投资价值企业TOP100。
公司主要从事输液、冻干、粉针、小水针、采血、中药复方制剂用各类“华兰”牌胶塞和软袋接口叁组件、塑瓶接口叁组件、塑料输液容器用聚异戊二烯橡胶垫片等的制造和销售。
华兰股份目前注册资本为1.1亿元人民币，总资产逾6亿元。拥有两家全资子公司：重庆市涪陵叁海兰陵有限责任公司——为响应国家支援西部开发，1998年，公司出资与重庆长丰通讯有限公司共同投资组建重庆市涪陵叁海兰陵责任有限公司。2002年7月，由江阴兰陵瓶塞有限公司和江阴硅氟塑料厂整体收购。2009年改制成为江苏华兰药用新材料股份有限公司全资法人控股公司，是华兰股份旗下专业从事药用丁基橡胶瓶塞研究和生产的核心企业，现已成为西部地区规模最大的药用丁基橡胶瓶塞制造企业；江苏华杨医疗科技有限公司——华兰股份旗下主要从事生物制品和二类6809泌尿肛肠微创外科手术器械的研究、开发。
华兰发展过程中一直坚持“华兰产品等于药品，华兰责任安全有效”的质量方针，把产品质量作为企业第一生存法则， 1998年，公司率先在行业内通过ISO9001质量体系认证，2003年，公司作为药用胶塞行业唯一代表参与起草了由中国医药包装协会组织的《药品包装实用手册》，得到行业的广泛应用。公司华兰牌注射液用卤化丁基橡胶塞获江苏名牌产品称号，自主知识产权产品新型复膜药用丁基胶塞评国家四部委评为国家重点新产品。
在二十年的经营过程中，华兰逐渐形成良好的销售理念，公司以“有诚就有成”的理念与国内外客户进行业务合作，优质的产品、良好的服务使华兰股份在市场上树立了良好的形象，赢得广大客户的认可与信赖，公司的销售网络遍及世界各地并成功进军意大利、叙利亚、埃及、越南、巴基斯坦等国家。2010年度，全国80%药厂都和公司有业务往来，其中建立稳定合作的药厂有800多家。
在经营活动中，公司树立了“股东利益最大化，社会责任永久化，客户利益市场化”的经营理念。一直以来，公司高度重视构建自身的人才优势，不断吸引高层次人才加盟。在全国民营企业中，率先获准成立了药用包装材料研究所，与国内一家知名高分子材料学府建立了校企合作，并与南京航空航天大学经济与管理学院合作，将公司定为其就业实践基地，为企业的创新发展积蓄后备力量。
在企业管理中，公司不断寻求新的突破，2003年9月，为适应市场的激烈竞争，公司全面推行GMP管理，在保证生产正常进行的情况下，把 GMP 各项管理落实到具体的工作任务中去，使之不断科学化、标准化、规范化；2004年公司做出又一重大举措，全面启动ERP项目，企业在信息化管理上又迈出坚实的一步。
公司在发展壮大的同时，时刻不忘积极投身于社会公益福利事业和科学、教育、文化、卫生事业当中，公司设立华兰“扶贫帮困”基金200万元，每年向江阴慈善总会定额支付16万元，直至交满200万元。公司领导充分认识科学知识的重要性，尽其所能，捐赠江阴市二中10万元资金，与申港镇贫困学生华香同学结对助学，助贫困学生顺得完成学业。公司以民营科技企业的身份赞助的江阴“南北结对”活动共资助5名贫困学生等。
2008年，公司被江苏省科技厅、财政厅、国税局、地税局认定为高新技术企业。2009年，华兰股份引入建银国际医疗产业基金等一批战略投资者，成功完成股份制改造。2010年，公司与中投证券签署辅导、保荐协议，正式启动IPO进程。
江苏华兰药用新材料股份有限公司将始终以“以股东利益最大化、社会责任永久化、客户利益市场化”的公司宗旨，坚持“华兰产品等于药品，华兰产品安全有效”的质量方针，深化“诚信为本，人文团队，勇于创新，铸造品牌” 的经营理念，不断推动企业科技进步，力争早日进入世界行业前叁名。
        </div> </div> </section> <div class="vip-div" id="syrlist"> <section class="panel b-a"> <div class="tcaption"> <h3 class="title">最终受益人</h3> <span class="tbadge">2</span> <span class="ntag vip m-l-sm" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title="尊敬的会员，您正在使用高级特权">功能</span> <span class="watermark"></span> </div> <div class="cbase-mengban zzsy"> <div class="cbase-vip-kuang"> <div class="vip-top"> <div class="vip-title"> <div class="title">最终受益人</div> <div class="sub-title"><span>成为VIP会员 即可挖掘直接或间接拥有疑似超过25%公司股权的自然人或企业</span><a rel="nofollow" href="/vip">查看全部></a></div> </div> <div class="vip-buy-panel"> <div class="vip-year-list-in clearfix"> <div data-id="17" class="vip-kuang vip-year active"> <div class="price"> <span>720元</span> <span style="color: #F9552A">/</span>
                                        3年
                                    </div> <div class="origin-price">原价：2160元</div> <div class="vip-rec"></div> </div> <div data-id="7" class="vip-kuang vip-year"> <div class="price"> <span>540元</span> <span style="color: #F9552A">/</span>
                                        2年
                                    </div> <div class="origin-price">原价：1440元</div> </div> <div data-id="6" class="vip-kuang vip-year"> <div class="price"> <span>360元</span> <span style="color: #F9552A">/</span>
                                        1年
                                    </div> <div class="origin-price">原价：720元</div> </div> </div> <a data-toggle="modal" data-target="#loginModal" class="vip-btn" onclick="getCaptcha()">立即开通</a> <div class="vip-publicity">支付后可开发票</div> </div> </div> <div class="vip-pay-container"> <div class="step1"> <img class="demo-img" src="/material/theme/chacha/cms/v2/images/vip/zzsy.png"/> <a rel="nofollow" class="vip-demo-link" href="/firm_9cce0780ab7644008b73bc2120479d31.shtml">查看样例></a> </div> </div> </div> </div> </section> </div> <div class="vip-div" id="kzrtupu"> <section class="panel b-a"> <div class="tcaption"> <h3 class="title">实际控制人</h3> <span class="ntag vip m-l-sm" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title="尊敬的会员，您正在使用高级特权">功能</span> <span class="watermark"></span> </div> <div class="cbase-mengban kzrt"> <div class="cbase-vip-kuang"> <div class="vip-top"> <div class="vip-title"> <div class="title">实际控制人</div> <div class="sub-title"><span>成为VIP会员即可查看疑似实际控制人  总股权比例等信息</span><a rel="nofollow" href="/vip">查看全部></a></div> </div> <div class="vip-buy-panel"> <div class="vip-year-list-in clearfix"> <div data-id="17" class="vip-kuang vip-year active"> <div class="price"> <span>720元</span> <span style="color: #F9552A">/</span>
                                        3年
                                    </div> <div class="origin-price">原价：2160元</div> <div class="vip-rec"></div> </div> <div data-id="7" class="vip-kuang vip-year"> <div class="price"> <span>540元</span> <span style="color: #F9552A">/</span>
                                        2年
                                    </div> <div class="origin-price">原价：1440元</div> </div> <div data-id="6" class="vip-kuang vip-year"> <div class="price"> <span>360元</span> <span style="color: #F9552A">/</span>
                                        1年
                                    </div> <div class="origin-price">原价：720元</div> </div> </div> <a data-toggle="modal" data-target="#loginModal" class="vip-btn" onclick="getCaptcha()">立即开通</a> <div class="vip-publicity">支付后可开发票</div> </div> </div> <div class="vip-pay-container"> <div class="step1"> <img class="demo-img" src="/material/theme/chacha/cms/v2/images/vip/kzrt2.png"/> <a rel="nofollow" class="vip-demo-link" href="/firm_9cce0780ab7644008b73bc2120479d31.shtml">查看样例></a> </div> </div> </div> </div> </section> </div> <div class="vip-div" id="holdcolist"> <section class="panel b-a"> <div class="tcaption"> <h3 class="title m-l-sm">控股企业</h3> <span class="tbadge">6</span> <span class="ntag vip m-l-sm" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title="尊敬的会员，您正在使用高级特权">功能</span> <span class="watermark"></span> </div> <div class="cbase-mengban kgqy"> <div class="cbase-vip-kuang"> <div class="vip-top"> <div class="vip-title"> <div class="title">控股企业</div> <div class="sub-title"><span>成为VIP会员 即可挖掘公司或自然人直接或间接拥有其疑似实际控制权的企业</span><a rel="nofollow" href="/vip">查看全部></a></div> </div> <div class="vip-buy-panel"> <div class="vip-year-list-in clearfix"> <div data-id="17" class="vip-kuang vip-year active"> <div class="price"> <span>720元</span> <span style="color: #F9552A">/</span>
                                        3年
                                    </div> <div class="origin-price">原价：2160元</div> <div class="vip-rec"></div> </div> <div data-id="7" class="vip-kuang vip-year"> <div class="price"> <span>540元</span> <span style="color: #F9552A">/</span>
                                        2年
                                    </div> <div class="origin-price">原价：1440元</div> </div> <div data-id="6" class="vip-kuang vip-year"> <div class="price"> <span>360元</span> <span style="color: #F9552A">/</span>
                                        1年
                                    </div> <div class="origin-price">原价：720元</div> </div> </div> <a data-toggle="modal" data-target="#loginModal" class="vip-btn" onclick="getCaptcha()">立即开通</a> <div class="vip-publicity">支付后可开发票</div> </div> </div> <div class="vip-pay-container"> <div class="step1"> <img class="demo-img" src="/material/theme/chacha/cms/v2/images/vip/kgqy.png"/> <a rel="nofollow" class="vip-demo-link" href="/firm_9cce0780ab7644008b73bc2120479d31.shtml">查看样例></a> </div> </div> </div> </div> </section> </div> <div class="vip-div" id="cwjx"> <section class="panel b-a"> <div class="tcaption"> <h3 class="title m-l-sm">财务简析</h3> <span class="ntag vip m-l-sm" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title="尊敬的会员，您正在使用高级特权">功能</span> <span class="watermark"></span> </div> <div class="cbase-mengban cwjx"> <div class="cbase-vip-kuang"> <div class="vip-top"> <div class="vip-title"> <div class="title">财务简析</div> <div class="sub-title"><span>成为VIP会员 即可查看企业营业收入、净利润、总资产、净资产、净利率、毛利率等</span><a rel="nofollow" href="/vip">查看全部></a></div> </div> <div class="vip-buy-panel"> <div class="vip-year-list-in clearfix"> <div data-id="17" class="vip-kuang vip-year active"> <div class="price"> <span>720元</span> <span style="color: #F9552A">/</span>
                                        3年
                                    </div> <div class="origin-price">原价：2160元</div> <div class="vip-rec"></div> </div> <div data-id="7" class="vip-kuang vip-year"> <div class="price"> <span>540元</span> <span style="color: #F9552A">/</span>
                                        2年
                                    </div> <div class="origin-price">原价：1440元</div> </div> <div data-id="6" class="vip-kuang vip-year"> <div class="price"> <span>360元</span> <span style="color: #F9552A">/</span>
                                        1年
                                    </div> <div class="origin-price">原价：720元</div> </div> </div> <a data-toggle="modal" data-target="#loginModal" class="vip-btn" onclick="getCaptcha()">立即开通</a> <div class="vip-publicity">支付后可开发票</div> </div> </div> <div class="vip-pay-container"> <div class="step1"> <img class="demo-img" src="/material/theme/chacha/cms/v2/images/vip/cwjx.png"/> <a rel="nofollow" class="vip-demo-link" href="/firm_9cce0780ab7644008b73bc2120479d31.shtml">查看样例></a> </div> </div> </div> </div> </section> </div> <div class="vip-div" id="thyfx"> <section class="panel b-a"> <div class="tcaption"> <h3 class="title m-l-sm">同业分析</h3> <span class="ntag vip m-l-sm" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title="尊敬的会员，您正在使用高级特权">功能</span> <span class="watermark"></span> </div> <div class="cbase-mengban tyfx"> <div class="cbase-vip-kuang"> <div class="vip-top"> <div class="vip-title"> <div class="title">同业分析</div> <div class="sub-title"><span>成为VIP会员 即可查看该企业在全国和本省范围内的同行业发展情况</span><a rel="nofollow" href="/vip">查看全部></a></div> </div> <div class="vip-buy-panel"> <div class="vip-year-list-in clearfix"> <div data-id="17" class="vip-kuang vip-year active"> <div class="price"> <span>720元</span> <span style="color: #F9552A">/</span>
                                        3年
                                    </div> <div class="origin-price">原价：2160元</div> <div class="vip-rec"></div> </div> <div data-id="7" class="vip-kuang vip-year"> <div class="price"> <span>540元</span> <span style="color: #F9552A">/</span>
                                        2年
                                    </div> <div class="origin-price">原价：1440元</div> </div> <div data-id="6" class="vip-kuang vip-year"> <div class="price"> <span>360元</span> <span style="color: #F9552A">/</span>
                                        1年
                                    </div> <div class="origin-price">原价：720元</div> </div> </div> <a data-toggle="modal" data-target="#loginModal" class="vip-btn" onclick="getCaptcha()">立即开通</a> <div class="vip-publicity">支付后可开发票</div> </div> </div> <div class="vip-pay-container"> <div class="step1"> <img class="demo-img" src="/material/theme/chacha/cms/v2/images/vip/tyfx.png"/> <a rel="nofollow" class="vip-demo-link" href="/firm_9cce0780ab7644008b73bc2120479d31.shtml">查看样例></a> </div> </div> </div> </div> </section> </div> <section class="panel b-a clear"> <div class="m_ptsc" style="padding:20px 0;">数据来源：国家企业信用信息公示系统。</div> </section> <script type="text/javascript">


  

setTimeout(function(){
    var touziIndustry = JSON.parse('[{"value":"C","desc":"\u5236\u9020\u4e1a","count":1},{"value":"F","desc":"\u6279\u53d1\u548c\u96f6\u552e\u4e1a","count":3},{"value":"M","desc":"\u79d1\u5b66\u7814\u7a76\u548c\u6280\u672f\u670d\u52a1\u4e1a","count":2}]');
    var touziProvince = JSON.parse('[{"value":"CQ","count":3,"desc":"\u91cd\u5e86"},{"value":"JS","count":3,"desc":"\u6c5f\u82cf"}]');
    var partners;
    try{
      partners = JSON.parse('[{"Org":0,"KeyNo":"bd51fff24d81b86140676e21b599e93a","HasImage":false,"CompanyCount":6,"StockName":"\u6c5f\u9634\u534e\u5170\u673a\u7535\u79d1\u6280\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"40.71%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320281000000450","ShouldCapi":"3582.857","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"3582.857","CapiDate":"2009-10-15","StockPercentValue":40.71,"ShouldCapiAmount":3582.857,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/bd51fff24d81b86140676e21b599e93a.jpg?x-oss-process=image\/resize,w_120","Tags":["\u5927\u80a1\u4e1c"],"FinalBenefitPercent":"42.249%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":2,"KeyNo":"p5748c03313a9627f6931d7a4248c06e","HasImage":false,"CompanyCount":14,"StockName":"\u534e\u4e00\u654f","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"25.00%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"2200","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"2200","CapiDate":"2009-10-15","StockPercentValue":25,"ShouldCapiAmount":2200,"Tags":["\u6700\u7ec8\u53d7\u76ca\u4eba"],"FinalBenefitPercent":"33.4498%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":0,"KeyNo":"2afa54af1435e871bc11ecac6a2c764e","HasImage":false,"CompanyCount":2,"StockName":"\u5efa\u94f6\u56fd\u9645\u533b\u7597\u4fdd\u5065\u6295\u8d44\u7ba1\u7406\uff08\u5929\u6d25\uff09\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"6.25%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"120191000037123","ShouldCapi":"550","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"550","CapiDate":"2009-10-15","StockPercentValue":6.25,"ShouldCapiAmount":550,"Invest":{"Id":"f016e59c7ad8b1d72903bb1aa5720d53","Name":"\u5efa\u94f6\u56fd\u9645\u8d22\u5bcc\u7ba1\u7406","Logo":"http:\/\/img.qichacha.com\/Investment\/logo\/f016e59c7ad8b1d72903bb1aa5720d53.jpg","NC":0,"FC":5},"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/2afa54af1435e871bc11ecac6a2c764e.jpg?x-oss-process=image\/resize,w_120","Tags":[],"FinalBenefitPercent":"6.25%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":0,"KeyNo":"c66d2d6d3f2e5543f2e2c96a94b37687","HasImage":false,"CompanyCount":1,"StockName":"\u82cf\u5dde\u6c7e\u6e56\u521b\u4e1a\u6295\u8d44\u80a1\u4efd\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"4.00%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320500000060705","ShouldCapi":"352.0174","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"352.0174","CapiDate":"2009-10-15","StockPercentValue":4,"ShouldCapiAmount":352.0174,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/c66d2d6d3f2e5543f2e2c96a94b37687.jpg?x-oss-process=image\/resize,w_120","Tags":[],"FinalBenefitPercent":"4.00%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":0,"KeyNo":"6feb1eb7aa183d36f7ab89fefd407e00","HasImage":true,"CompanyCount":42,"StockName":"\u6c5f\u82cf\u5eb7\u7f18\u96c6\u56e2\u6709\u9650\u8d23\u4efb\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"3.43%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320700000029477","ShouldCapi":"302.1609","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"302.1609","CapiDate":"2009-10-15","StockPercentValue":3.43,"ShouldCapiAmount":302.1609,"ImageUrl":"https:\/\/co-image.qichacha.com\/CompanyImage\/6feb1eb7aa183d36f7ab89fefd407e00.jpg?x-oss-process=style\/qcc_cmp","Tags":[],"FinalBenefitPercent":"3.43%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":0,"KeyNo":"3c14dc3d45e9416a07ce9af92aa6fc34","HasImage":false,"CompanyCount":1,"StockName":"\u6c5f\u9634\u534e\u6052\u6295\u8d44\u7ba1\u7406\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"1.84%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320281000245847","ShouldCapi":"162.1597","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"162.1597","CapiDate":"2009-10-15","StockPercentValue":1.84,"ShouldCapiAmount":162.1597,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/3c14dc3d45e9416a07ce9af92aa6fc34.jpg?x-oss-process=image\/resize,w_120","Tags":[],"FinalBenefitPercent":"1.84%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":0,"KeyNo":"0cf3e80f168626ac2d10ebde96ef59c8","HasImage":false,"CompanyCount":1,"StockName":"\u6c5f\u9634\u534e\u5e73\u6295\u8d44\u7ba1\u7406\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"1.71%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320281000244268","ShouldCapi":"150.0732","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"150.0732","CapiDate":"2009-10-15","StockPercentValue":1.71,"ShouldCapiAmount":150.0732,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/0cf3e80f168626ac2d10ebde96ef59c8.jpg?x-oss-process=image\/resize,w_120","Tags":[],"FinalBenefitPercent":"1.71%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false}]');
    }catch(e){
      partners = [{"Org":0,"KeyNo":"bd51fff24d81b86140676e21b599e93a","HasImage":false,"CompanyCount":6,"StockName":"\u6c5f\u9634\u534e\u5170\u673a\u7535\u79d1\u6280\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"40.71%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320281000000450","ShouldCapi":"3582.857","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"3582.857","CapiDate":"2009-10-15","StockPercentValue":40.71,"ShouldCapiAmount":3582.857,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/bd51fff24d81b86140676e21b599e93a.jpg?x-oss-process=image\/resize,w_120","Tags":["\u5927\u80a1\u4e1c"],"FinalBenefitPercent":"42.249%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":2,"KeyNo":"p5748c03313a9627f6931d7a4248c06e","HasImage":false,"CompanyCount":14,"StockName":"\u534e\u4e00\u654f","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"25.00%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"2200","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"2200","CapiDate":"2009-10-15","StockPercentValue":25,"ShouldCapiAmount":2200,"Tags":["\u6700\u7ec8\u53d7\u76ca\u4eba"],"FinalBenefitPercent":"33.4498%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":0,"KeyNo":"2afa54af1435e871bc11ecac6a2c764e","HasImage":false,"CompanyCount":2,"StockName":"\u5efa\u94f6\u56fd\u9645\u533b\u7597\u4fdd\u5065\u6295\u8d44\u7ba1\u7406\uff08\u5929\u6d25\uff09\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"6.25%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"120191000037123","ShouldCapi":"550","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"550","CapiDate":"2009-10-15","StockPercentValue":6.25,"ShouldCapiAmount":550,"Invest":{"Id":"f016e59c7ad8b1d72903bb1aa5720d53","Name":"\u5efa\u94f6\u56fd\u9645\u8d22\u5bcc\u7ba1\u7406","Logo":"http:\/\/img.qichacha.com\/Investment\/logo\/f016e59c7ad8b1d72903bb1aa5720d53.jpg","NC":0,"FC":5},"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/2afa54af1435e871bc11ecac6a2c764e.jpg?x-oss-process=image\/resize,w_120","Tags":[],"FinalBenefitPercent":"6.25%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":0,"KeyNo":"c66d2d6d3f2e5543f2e2c96a94b37687","HasImage":false,"CompanyCount":1,"StockName":"\u82cf\u5dde\u6c7e\u6e56\u521b\u4e1a\u6295\u8d44\u80a1\u4efd\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"4.00%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320500000060705","ShouldCapi":"352.0174","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"352.0174","CapiDate":"2009-10-15","StockPercentValue":4,"ShouldCapiAmount":352.0174,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/c66d2d6d3f2e5543f2e2c96a94b37687.jpg?x-oss-process=image\/resize,w_120","Tags":[],"FinalBenefitPercent":"4.00%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":0,"KeyNo":"6feb1eb7aa183d36f7ab89fefd407e00","HasImage":true,"CompanyCount":42,"StockName":"\u6c5f\u82cf\u5eb7\u7f18\u96c6\u56e2\u6709\u9650\u8d23\u4efb\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"3.43%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320700000029477","ShouldCapi":"302.1609","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"302.1609","CapiDate":"2009-10-15","StockPercentValue":3.43,"ShouldCapiAmount":302.1609,"ImageUrl":"https:\/\/co-image.qichacha.com\/CompanyImage\/6feb1eb7aa183d36f7ab89fefd407e00.jpg?x-oss-process=style\/qcc_cmp","Tags":[],"FinalBenefitPercent":"3.43%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":0,"KeyNo":"3c14dc3d45e9416a07ce9af92aa6fc34","HasImage":false,"CompanyCount":1,"StockName":"\u6c5f\u9634\u534e\u6052\u6295\u8d44\u7ba1\u7406\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"1.84%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320281000245847","ShouldCapi":"162.1597","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"162.1597","CapiDate":"2009-10-15","StockPercentValue":1.84,"ShouldCapiAmount":162.1597,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/3c14dc3d45e9416a07ce9af92aa6fc34.jpg?x-oss-process=image\/resize,w_120","Tags":[],"FinalBenefitPercent":"1.84%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false},{"Org":0,"KeyNo":"0cf3e80f168626ac2d10ebde96ef59c8","HasImage":false,"CompanyCount":1,"StockName":"\u6c5f\u9634\u534e\u5e73\u6295\u8d44\u7ba1\u7406\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"1.71%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320281000244268","ShouldCapi":"150.0732","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"150.0732","CapiDate":"2009-10-15","StockPercentValue":1.71,"ShouldCapiAmount":150.0732,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/0cf3e80f168626ac2d10ebde96ef59c8.jpg?x-oss-process=image\/resize,w_120","Tags":[],"FinalBenefitPercent":"1.71%","HasStockDetail":false,"HasStockFreezenInfo":false,"HasPledgeInfo":false}];
    }
     touziChart(touziIndustry,touziProvince);  //低于5个隐藏图表
    partnersChart(partners,'万元',38); //大于10个隐藏图表
    muhouIframe();
    showHistoryTip();
    drawGuquanStatic('江苏华兰药用新材料股份有限公司',[{"Org":0,"KeyNo":"bd51fff24d81b86140676e21b599e93a","HasImage":false,"CompanyCount":6,"StockName":"\u6c5f\u9634\u534e\u5170\u673a\u7535\u79d1\u6280\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"40.71%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320281000000450","ShouldCapi":"3582.857","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"3582.857","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":["\u5927\u80a1\u4e1c"],"FinalBenefitPercent":"42.249%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/bd51fff24d81b86140676e21b599e93a.jpg?x-oss-process=image\/resize,w_120","StockPercentNew":"40.71","bigPartner":true},{"Org":2,"KeyNo":"p5748c03313a9627f6931d7a4248c06e","HasImage":false,"CompanyCount":14,"StockName":"\u534e\u4e00\u654f","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"25.00%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"2200","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"2200","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":["\u6700\u7ec8\u53d7\u76ca\u4eba"],"FinalBenefitPercent":"33.4498%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"25.00","syr":true},{"Org":0,"KeyNo":"2afa54af1435e871bc11ecac6a2c764e","HasImage":false,"CompanyCount":2,"StockName":"\u5efa\u94f6\u56fd\u9645\u533b\u7597\u4fdd\u5065\u6295\u8d44\u7ba1\u7406\uff08\u5929\u6d25\uff09\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"6.25%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"120191000037123","ShouldCapi":"550","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"550","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"6.25%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/2afa54af1435e871bc11ecac6a2c764e.jpg?x-oss-process=image\/resize,w_120","StockPercentNew":"6.25","Invest":{"Id":"f016e59c7ad8b1d72903bb1aa5720d53","Name":"\u5efa\u94f6\u56fd\u9645\u8d22\u5bcc\u7ba1\u7406","Logo":"http:\/\/img.qichacha.com\/Investment\/logo\/f016e59c7ad8b1d72903bb1aa5720d53.jpg","NC":0,"FC":5}},{"Org":0,"KeyNo":"c66d2d6d3f2e5543f2e2c96a94b37687","HasImage":false,"CompanyCount":1,"StockName":"\u82cf\u5dde\u6c7e\u6e56\u521b\u4e1a\u6295\u8d44\u80a1\u4efd\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"4.00%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320500000060705","ShouldCapi":"352.0174","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"352.0174","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"4.00%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/c66d2d6d3f2e5543f2e2c96a94b37687.jpg?x-oss-process=image\/resize,w_120","StockPercentNew":"4.00"},{"Org":0,"KeyNo":"6feb1eb7aa183d36f7ab89fefd407e00","HasImage":true,"CompanyCount":42,"StockName":"\u6c5f\u82cf\u5eb7\u7f18\u96c6\u56e2\u6709\u9650\u8d23\u4efb\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"3.43%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320700000029477","ShouldCapi":"302.1609","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"302.1609","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"3.43%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"ImageUrl":"https:\/\/co-image.qichacha.com\/CompanyImage\/6feb1eb7aa183d36f7ab89fefd407e00.jpg?x-oss-process=style\/qcc_cmp","StockPercentNew":"3.43"},{"Org":0,"KeyNo":"3c14dc3d45e9416a07ce9af92aa6fc34","HasImage":false,"CompanyCount":1,"StockName":"\u6c5f\u9634\u534e\u6052\u6295\u8d44\u7ba1\u7406\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"1.84%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320281000245847","ShouldCapi":"162.1597","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"162.1597","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"1.84%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/3c14dc3d45e9416a07ce9af92aa6fc34.jpg?x-oss-process=image\/resize,w_120","StockPercentNew":"1.84"},{"Org":0,"KeyNo":"0cf3e80f168626ac2d10ebde96ef59c8","HasImage":false,"CompanyCount":1,"StockName":"\u6c5f\u9634\u534e\u5e73\u6295\u8d44\u7ba1\u7406\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"1.71%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"320281000244268","ShouldCapi":"150.0732","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"150.0732","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"1.71%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/0cf3e80f168626ac2d10ebde96ef59c8.jpg?x-oss-process=image\/resize,w_120","StockPercentNew":"1.71"},{"Org":2,"KeyNo":"p9f47a69983d2a70e2051593c10c8d7e","HasImage":false,"CompanyCount":18,"StockName":"\u5f90\u4e2d\u6770","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"1.60%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"141.0084","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"141.0084","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"1.60%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"1.60"},{"Org":2,"KeyNo":"pf4e287811dfaddd203ee351ffcd8e2b","HasImage":false,"CompanyCount":13,"StockName":"\u90ed\u987a\u534e","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"1.60%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"141.0084","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"141.0084","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"1.60%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"1.60"},{"Org":2,"KeyNo":"pbd8809988eaada153061b6c44b44d85","HasImage":false,"CompanyCount":3,"StockName":"\u9ec4\u4f1f\u56fd","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"1.53%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"134.9652","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"134.9652","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"1.53%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"1.53"},{"Org":0,"KeyNo":"3732e92d3deaadfb0a6ec0f45efe315a","HasImage":false,"CompanyCount":8,"StockName":"\u6cf0\u5dde\u745e\u6d0b\u7acb\u6cf0\u7cbe\u5316\u79d1\u6280\u6709\u9650\u516c\u53f8","StockType":"\u4f01\u4e1a\u6cd5\u4eba","StockPercent":"1.14%","IdentifyType":"\u4f01\u4e1a\u6cd5\u4eba\u8425\u4e1a\u6267\u7167(\u516c\u53f8)","IdentifyNo":"321200000013004","ShouldCapi":"100.7203","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"100.7203","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"1.14%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"ImageUrl":"https:\/\/qccdata.qichacha.com\/AutoImage\/3732e92d3deaadfb0a6ec0f45efe315a.jpg?x-oss-process=image\/resize,w_120","StockPercentNew":"1.14"},{"Org":2,"KeyNo":"p27093ec06e353427fa08a9db3dfcb9e","HasImage":true,"CompanyCount":77,"StockName":"\u5f90\u6c49\u6770","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"1.03%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"90.6483","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"90.6483","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"1.03%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"1.03"},{"Org":2,"KeyNo":"p428c82f04ba30464e461ed25a4f9d3b","HasImage":false,"CompanyCount":4,"StockName":"\u8d75\u6021\u65b0","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.97%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"85.6122","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"85.6122","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.97%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.97"},{"Org":2,"KeyNo":"p0eee4d776af76d98e206fc0ac03dcea","HasImage":false,"CompanyCount":3,"StockName":"\u5b59\u70b3\u8363","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.92%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"80.5762","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"80.5762","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.92%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.92"},{"Org":2,"KeyNo":"p6f7ab4759dd2e497028ba4b56775919","HasImage":true,"CompanyCount":40,"StockName":"\u6bb5\u5c0f\u5149","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.81%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"71.5114","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"71.5114","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.81%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.81"},{"Org":2,"KeyNo":"p3cc0d7eb1afec411b5e64bfea9cf0c2","HasImage":false,"CompanyCount":10,"StockName":"\u5f90\u5fd7\u541b","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.80%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"70.5042","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"70.5042","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.80%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.80"},{"Org":2,"KeyNo":"pa18f48637fb38a589fd3de7a91b3e3a","HasImage":false,"CompanyCount":6,"StockName":"\u59da\u5609","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.74%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"65.4682","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"65.4682","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.74%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.74"},{"Org":2,"KeyNo":"pdbb7562e928c58634ff16bf11474c44","HasImage":false,"CompanyCount":3,"StockName":"\u5510\u4fdd\u529b","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.74%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"65.4682","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"65.4682","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.74%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.74"},{"Org":2,"KeyNo":"pd3be8995fb5c391c42ffc9084dc10cb","HasImage":false,"CompanyCount":6,"StockName":"\u9b4f\u5dcd","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.57%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"50.3601","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"50.3601","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.57%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.57"},{"Org":2,"KeyNo":"p35aedd6f24d20eb8f4babb5119e16b4","HasImage":false,"CompanyCount":1,"StockName":"\u5f90\u5efa\u5174","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.46%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"40.2881","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"40.2881","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.46%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.46"},{"Org":2,"KeyNo":"p208b2e1256d06645a0672ba93afe4a0","HasImage":false,"CompanyCount":7,"StockName":"\u5f20\u542f\u65b9","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.40%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"35.2521","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"35.2521","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.40%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.40"},{"Org":2,"KeyNo":"p657d92bb60e174f5a73fba63df9764c","HasImage":false,"CompanyCount":5,"StockName":"\u4f55\u6587\u4f1f","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.40%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"35.2521","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"35.2521","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.40%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.40"},{"Org":2,"KeyNo":"p9aa63dbcee79bbcbe102774e0ca892d","HasImage":false,"CompanyCount":17,"StockName":"\u9ec4\u7fe0\u5a1f","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.40%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"35.2521","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"35.2521","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.40%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.40"},{"Org":2,"KeyNo":"p119fcdaa9e17e311be0f58cc8058fb3","HasImage":false,"CompanyCount":1,"StockName":"\u5218\u7ea2\u536b","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.34%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"30.2161","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"30.2161","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.34%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.34"},{"Org":2,"KeyNo":"p86d1a4ba07b23530aa5bf35d7c8f3b4","HasImage":false,"CompanyCount":3,"StockName":"\u674e\u79c0","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.34%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"30.2161","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"30.2161","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.34%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.34"},{"Org":2,"KeyNo":"p73c2a4d9e1560be87f939f6d74fae4d","HasImage":false,"CompanyCount":3,"StockName":"\u9ad8\u96c6\u99a5","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.32%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"28.2017","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"28.2017","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.32%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.32"},{"Org":2,"KeyNo":"p0ac85ba23e4e4d9ab40ac9cc47b5603","HasImage":false,"CompanyCount":2,"StockName":"\u6731\u660e","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.19%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"17.1224","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"17.1224","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.19%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.19"},{"Org":2,"KeyNo":"p252fd81e01748dedfcd92b219584cd5","HasImage":false,"CompanyCount":3,"StockName":"\u6768\u745e\u82ac","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.19%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"17.1224","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"17.1224","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.19%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.19"},{"Org":2,"KeyNo":"p9d5feacf1b29f647d26dd5b80a24466","HasImage":false,"CompanyCount":1,"StockName":"\u9648\u7434\u82ac","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.19%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"17.1224","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"17.1224","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.19%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.19"},{"Org":2,"KeyNo":"pc430b08e72f9006cbdda9331f4cf3c5","HasImage":false,"CompanyCount":3,"StockName":"\u6bb7\u6d2a\u6797","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.19%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"17.1224","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"17.1224","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.19%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.19"},{"Org":2,"KeyNo":"p91ad9d336c1521a7e3e851100031eaa","HasImage":false,"CompanyCount":1,"StockName":"\u738b\u7389\u73e0","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.17%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"15.108","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"15.108","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.17%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.17"},{"Org":2,"KeyNo":"p95360910802739414ed7fa9f0925e0f","HasImage":false,"CompanyCount":1,"StockName":"\u9ec4\u963f\u7115","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.16%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"14.1008","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"14.1008","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.16%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.16"},{"Org":2,"KeyNo":"pd8e32622f52f1899c01d248ef35b5b1","HasImage":false,"CompanyCount":3,"StockName":"\u6bb7\u84c9\u8f89","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.16%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"14.1008","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"14.1008","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.16%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.16"},{"Org":2,"KeyNo":"pe4796b4750435050e60b8d9f5f298fd","HasImage":false,"CompanyCount":5,"StockName":"\u5b5f\u6631","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.16%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"14.1008","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"14.1008","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.16%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.16"},{"Org":2,"KeyNo":"p516d6e59c0babdd55d8526356102ead","HasImage":false,"CompanyCount":3,"StockName":"\u674e\u5a1f","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.14%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"12.0864","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"12.0864","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.14%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.14"},{"Org":2,"KeyNo":"p904ea083f2bae72a2b5e2df256e90ba","HasImage":false,"CompanyCount":1,"StockName":"\u8bb8\u4e00\u82b1","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.11%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"10.072","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"10.072","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.11%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.11"},{"Org":2,"KeyNo":"pca5e2cea8eb6417432aa1e79dce7401","HasImage":false,"CompanyCount":2,"StockName":"\u6731\u51ef","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.11%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"10.072","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"10.072","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.11%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.11"},{"Org":2,"KeyNo":"pd8cd500e5f73487fa0988000c1367b4","HasImage":false,"CompanyCount":5,"StockName":"\u535c\u5fe0\u5174","StockType":"\u81ea\u7136\u4eba\u80a1\u4e1c","StockPercent":"0.11%","IdentifyType":"\u975e\u516c\u793a\u9879","IdentifyNo":null,"ShouldCapi":"10.072","ShoudDate":"2009-10-15","InvestType":null,"InvestName":null,"RealCapi":"10.072","CapiDate":"2009-10-15","HasStockDetail":false,"Tags":[],"FinalBenefitPercent":"0.11%","HasStockFreezenInfo":false,"HasPledgeInfo":false,"StockPercentNew":"0.11"}]);
    $('body').on('click','.sanbanGd a',function(){
        var date = $(this).attr('data-value');
        $.ajax({
            type:'get',
            url:INDEX_URL + '/company_getSanbanGd',
            data:{code:'',date:date},
            dataType:'html',
            success:function(data){
                if(data){
                    $('#ipoSockinfo').html(data);
                    //$.scrollTo('#ipoSockinfo',{duration: 100, offset: -60});
                }
            }
        })
    });
  },500);
</script> </div> </div> <div class="col-sm-3 m_rightPanels"> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()" class="right-certpic"> <span class="btn btn-primary">立即认证</span> </a> <section class="panel b-a n-s qa-section" style="display: none;"> <div class="panel-heading b-b bg-blue"> <span class="font-bold font-15"><h2 class="text-primary">企业公告</h2></span> </div> <ul class="list-group no-bg auto" id="noticeRight"> </ul> </section> <section class="panel b-a n-s qa-section" id="qaRightAsk"> <div class="panel-heading bg-blue" style="border-bottom: none;"> <img class="qa_lo" src="/material/theme/chacha/cms/v2/images/qa_lo.png"><span>想了解更多这家企业的信息吗？</span> </div> <div class="panel-body" style="background: #F3F9FE;"> <div class="clearfix ask-footer active"> <input type="hidden" name="keyno" value="5f981c1538705fe2ec4891565b370edc"/> <div class="textarea-count"> <textarea placeholder="写下你的问题" maxlength="100" rows="3" class="textarea"></textarea> <span class="wordwrap" style="display: none;"><span class="wordCount">0</span>/<span class="maxCount">100</span></span> <a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('问答模块按钮点击',{'按钮名称':'提问按钮'});" class="btn btn-primary">提问</a> </div> </div> </div> <ul class="list-group no-bg auto qa-ul-list company-ul" id="companyUlQa"> <a class="list-group-item clearfix"> <div class="question"> <span class="icon"></span><div class="title"></div> <div class="count"><span class="text-danger"></span></div> </div> <div class="answer"> <span class="icon"></span> </div> </a> <a class="list-group-item clearfix"> <div class="question"> <span class="icon"></span><div class="title"></div> <div class="count"><span class="text-danger"></span></div> </div> <div class="answer"> <span class="icon"></span> </div> </a> </ul> <div class="more" style="display: none;"> <a rel="nofollow" onclick="zhugeTrack('问答模块按钮点击',{'按钮名称':'查看全部问答'});" class="text-primary" href="https://pinpai.qichacha.com/own_5f981c1538705fe2ec4891565b370edc.html#qalist">查看全部<span id="companyUlQaCount"></span>个问答></a> </div> </section> <section class="panel b-a n-s qa-section" style="display: none;"> <div class="panel-heading b-b bg-blue"> <span class="font-bold font-15"><h2 class="text-primary">本企业相关问答</h2></span> </div> </section> <section class="panel b-a n-s qa-section" style="display: none;"> <div class="panel-heading b-b"> <span class="font-bold font-15"><h2>热门问答</h2></span> </div> <ul class="list-group no-bg auto qa-ul-list" id="hotUlQa"> <li class="list-group-item clearfix"> <div class="title m-b"> <img class="logo m-r-sm" src="https://co-image.qichacha.com/CompanyImage/f625a5b661058ba5082ca508f99ffe1b.jpg?x-oss-process=style/qcc_cmp"> <a href="">苏州朗动网络科技有限公司</a> </div> <div class="question"> <span class="icon"></span> <div class="count"><span class="text-danger"></span></div> </div> <div class="answer"> <span class="icon"></span> </div> </li> </ul> <div class="more"> <a onclick="zhugeTrack('问答模块按钮点击',{'按钮名称':'热门问答全部问答'});" rel="nofollow" class="text-primary" href="/more_hotqa">查看更多热门问答></a> </div> </section> <script type="text/javascript">
    
    $(function(){

        
        gethotqa();

        
        getcompanyqa('5f981c1538705fe2ec4891565b370edc');
        statInputNum($('#qaRightAsk .textarea-count'),100);
        // $('#qaRightAsk .textarea').on('focus',function(){
        //     $('#qaRightAsk .ask-footer').addClass('active');
        // })
        // $('#qaRightAsk .textarea').on('blur',function(){
        //     if(!this.value){
        //         $('#qaRightAsk .ask-footer').removeClass('active');
        //     }
        // })
            })
   
    
</script> <div id="promoteRight"></div> <div class="panel b-a n-s" id="fapiao-title"> <div class="panel-heading b-b btab"> <a href="#qiyeQrcode" onclick="changeQrTAB(1,this);zhugeTrack('企业主页-在手机中查看',{'企业名称':'江苏华兰药用新材料股份有限公司'});" data-toggle="tab"><h2>在手机中查看</h2></a> <a href="#fapiaoQrcode" onclick="changeQrTAB(2,this);zhugeTrack('企业主页-保存发票抬头',{'企业名称':'江苏华兰药用新材料股份有限公司'});" data-toggle="tab" class="active"><h2>保存发票抬头</h2></a> </div> <div class="panel-body text-center"> <div id="qiyeQrcode" style="display: none;"> <div id="qiye_taitou" class="m_qrp"></div> <div class="m-t-xs text-dark m-b"><a rel="nofollow" href="/app" target="_blank" class="text-primary">企查查APP</a> 扫一扫查看企业详情</div> </div> <div id="fapiaoQrcode"> <a rel="nofollow" id="fapiao_taitou" class="m_qrp" href="/tax_view?keyno=5f981c1538705fe2ec4891565b370edc"> </a> <div class="m-t-xs text-dark"><a rel="nofollow" href="/app" target="_blank" class="text-primary">企查查APP</a> 扫一扫保存发票抬头</div> <div class="m-t-md TaxView" style="display: none"> <p class="text-left">名称&nbsp;:&nbsp;<span class="Name"></span></p> <p class="text-left">税号&nbsp;:&nbsp;<span class="CreditCode"></span></p> <p class="text-left">地址&nbsp;:&nbsp;<span class="Address"></span></p> <p class="text-left">电话&nbsp;:&nbsp;<span class="PhoneNumber"></span></p> <p class="text-left">开户银行&nbsp;:&nbsp;<span class="Bank"></span></p> <p class="text-left">银行账户&nbsp;:&nbsp;<span class="Bankaccount"></span></p> </div> </div> </div> </div> <section class="panel b-a n-s"> <div class="panel-heading b-b"> <span class="font-bold font-15 text-dark"><h2>最新动态</h2></span> <a class="pull-right v3e_more" href="/crun_5f981c1538705fe2ec4891565b370edc#newslistByjob" id="job_title" >查看更多></a> </div> <ul class="list-group no-bg auto"> <a href="https://news.qichacha.com/postnews_0d7e73c447152ca36feb59b337d907f6.html" target="_blank" class="list-group-item clearfix"> <span class="clear"> <span>江阴成立生命健康产业技术创新战略联盟</span> </span> <span class="text-muted text-xs"><i class="i i-clock"></i> 2019-10-29</span> <span class="pull-right text-muted text-xs" style="padding: 4px">网易号</span> </a> <a href="https://news.qichacha.com/postnews_4d23403951162ff1ce63c680c7c44cd7.html" target="_blank" class="list-group-item clearfix"> <span class="clear"> <span>江阴市人大代表申港小组开展“履职活动周”活动</span> </span> <span class="text-muted text-xs"><i class="i i-clock"></i> 2019-10-01</span> <span class="pull-right text-muted text-xs" style="padding: 4px">今日头条</span> </a> <a href="https://news.qichacha.com/postnews_3154ebe1d1875c43ab3806fab3d0ca76.html" target="_blank" class="list-group-item clearfix"> <span class="clear"> <span>市领导参加市人大代表“履职活动周”专题视察活动</span> </span> <span class="text-muted text-xs"><i class="i i-clock"></i> 2019-09-30</span> <span class="pull-right text-muted text-xs" style="padding: 4px">今日头条</span> </a> <a href="https://news.qichacha.com/postnews_50fd989546164125f79b053456a50763.html" target="_blank" class="list-group-item clearfix"> <span class="clear"> <span>靠一枚小小的药用丁基橡胶塞，竟然走出了国门！这家涪陵企业有点角！</span> </span> <span class="text-muted text-xs"><i class="i i-clock"></i> 2019-06-25</span> <span class="pull-right text-muted text-xs" style="padding: 4px">涪陵生活圈</span> </a> <a href="https://news.qichacha.com/postnews_966f817cdad139a24fda367b4b0ee667.html" target="_blank" class="list-group-item clearfix"> <span class="clear"> <span>华泰联合关于华兰股份上市辅导的反馈：尚存部分未办理房产 其他情况正常</span> </span> <span class="text-muted text-xs"><i class="i i-clock"></i> 2018-10-12</span> <span class="pull-right text-muted text-xs" style="padding: 4px">中金证券</span> </a> </ul> </section> <section class="panel b-a n-s"> <div class="panel-heading b-b"> <span class="font-bold font-15 text-dark"><h2>您可能感兴趣的企业</h2></span> </div> <ul class="list-group no-bg auto"> <a onclick="zhugeTrack('企业主页-您可能感兴趣的企业',{'企业名称':'宁波虹霖进出口有限公司'});" href="/firm_b29de55c4d6358fdf4cf0a8611cb351d.html" class="list-group-item clearfix"> <span class="clear"> <span>宁波虹霖进出口有限公司</span><br/> </span> </a> <a onclick="zhugeTrack('企业主页-您可能感兴趣的企业',{'企业名称':'小米科技有限责任公司'});" href="/firm_9cce0780ab7644008b73bc2120479d31.html" class="list-group-item clearfix"> <span class="clear"> <span>小米科技有限责任公司</span><br/> </span> </a> <a onclick="zhugeTrack('企业主页-您可能感兴趣的企业',{'企业名称':'克拉玛依区月亮湾按摩店'});" href="/firm_f38d49e55533db9dfd0e06ac1ef38a8c.html" class="list-group-item clearfix"> <span class="clear"> <span>克拉玛依区月亮湾按摩店</span><br/> </span> </a> <a onclick="zhugeTrack('企业主页-您可能感兴趣的企业',{'企业名称':'湖北华网通信集团有限公司武汉分公司'});" href="/firm_5cf17c2eb47c27d7157ad83ee33a21fc.html" class="list-group-item clearfix"> <span class="clear"> <span>湖北华网通信集团有限公司武汉分公司</span><br/> </span> </a> <a onclick="zhugeTrack('企业主页-您可能感兴趣的企业',{'企业名称':'洛阳泰明鸿科技有限公司'});" href="/firm_caab99b8ce1203d66c350571a14baabd.html" class="list-group-item clearfix"> <span class="clear"> <span>洛阳泰明鸿科技有限公司</span><br/> </span> </a> </ul> </section> <section class="panel b-a n-s "> <div class="panel-heading b-b"> <span class="font-bold font-15 text-dark"><h2>同地区同行业企业</h2></span> </div> <ul class="list-group no-bg auto boss-partners"> <li class="list-group-item clearfix"> <div class="title"> <div class="head"> <img class="usericon partner-letter" src="https://qccdata.qichacha.com/AutoImage/df3e2d7455355d7a5b75edbe5cb55de6.jpg?x-oss-process=image/resize,w_120" onerror="this.src='https://co-image.qichacha.com/CompanyImage/default.jpg'"> </div> <div class="name same-property-ellipsis"> <a class="same-property-top" href="/firm_df3e2d7455355d7a5b75edbe5cb55de6.html">江阴市曹氏纺织器材有限公司</a> </div> <div class="content same-property-ellipsis"> <a class="same-property-bottom" href="/pl_pf967bcd2c0362b46b8c5b3c107c0e62.html">曹建璋</a> </div> </div> </li> <li class="list-group-item clearfix"> <div class="title"> <div class="head"> <img class="usericon partner-letter" src="https://co-image.qichacha.com/CompanyImage/ddf51ac2e2b52fd9f37ecabfe048efe9.jpg?x-oss-process=image/resize,w_160" onerror="this.src='https://co-image.qichacha.com/CompanyImage/default.jpg'"> </div> <div class="name same-property-ellipsis"> <a class="same-property-top" href="/firm_ddf51ac2e2b52fd9f37ecabfe048efe9.html">江阴市安基橡胶工业有限公司</a> </div> <div class="content same-property-ellipsis"> <a class="same-property-bottom" href="/pl_p4cd1f1f5cc13cbf06f397f0c59f5ae1.html">刘燕明</a> </div> </div> </li> <li class="list-group-item clearfix"> <div class="title"> <div class="head"> <img class="usericon partner-letter" src="https://qccdata.qichacha.com/AutoImage/de90a8e02361ab6a49fd44e32407a5eb.jpg?x-oss-process=image/resize,w_120" onerror="this.src='https://co-image.qichacha.com/CompanyImage/default.jpg'"> </div> <div class="name same-property-ellipsis"> <a class="same-property-top" href="/firm_de90a8e02361ab6a49fd44e32407a5eb.html">宜兴市申达衬胶有限公司</a> </div> <div class="content same-property-ellipsis"> <a class="same-property-bottom" href="/pl_p1e8f84a2901be79af53a24850dfe31b.html">李申甲</a> </div> </div> </li> <li class="list-group-item clearfix"> <div class="title"> <div class="head"> <img class="usericon partner-letter" src="https://qccdata.qichacha.com/AutoImage/de5530a2de6d76625e0691d7fa4db96e.jpg?x-oss-process=image/resize,w_120" onerror="this.src='https://co-image.qichacha.com/CompanyImage/default.jpg'"> </div> <div class="name same-property-ellipsis"> <a class="same-property-top" href="/firm_de5530a2de6d76625e0691d7fa4db96e.html">江阴市大桥塑胶密封件厂</a> </div> <div class="content same-property-ellipsis"> <a class="same-property-bottom" href="/pl_p82f859463fc3d668a6e1fb8eb5f33ab.html">韩国兴</a> </div> </div> </li> <li class="list-group-item clearfix"> <div class="title"> <div class="head"> <img class="usericon partner-letter" src="https://qccdata.qichacha.com/AutoImage/de2e789d7e03ca5ac535c7aba85f4153.jpg?x-oss-process=image/resize,w_120" onerror="this.src='https://co-image.qichacha.com/CompanyImage/default.jpg'"> </div> <div class="name same-property-ellipsis"> <a class="same-property-top" href="/firm_de2e789d7e03ca5ac535c7aba85f4153.html">江阴市闵氏球业有限公司</a> </div> <div class="content same-property-ellipsis"> <a class="same-property-bottom" href="/pl_p2b136243acbbce20abc5eba18fbb347.html">闵惠义</a> </div> </div> </li> <li class="list-group-item clearfix"> <div class="title"> <div class="head"> <img class="usericon partner-letter" src="https://qccdata.qichacha.com/AutoImage/de088dce72ca9a8356d24c1b5e67f09b.jpg?x-oss-process=image/resize,w_120" onerror="this.src='https://co-image.qichacha.com/CompanyImage/default.jpg'"> </div> <div class="name same-property-ellipsis"> <a class="same-property-top" href="/firm_de088dce72ca9a8356d24c1b5e67f09b.html">无锡世信胶粘带制品有限公司</a> </div> <div class="content same-property-ellipsis"> <a class="same-property-bottom" href="/pl_pc2f469e97240119b595ccb709cc294b.html">方建伟</a> </div> </div> </li> <li class="list-group-item clearfix"> <div class="title"> <div class="head"> <img class="usericon partner-letter" src="https://qccdata.qichacha.com/AutoImage/ddc28639aa737bbd1926fb598ea9821e.jpg?x-oss-process=image/resize,w_120" onerror="this.src='https://co-image.qichacha.com/CompanyImage/default.jpg'"> </div> <div class="name same-property-ellipsis"> <a class="same-property-top" href="/firm_ddc28639aa737bbd1926fb598ea9821e.html">无锡诚盛制带有限公司</a> </div> <div class="content same-property-ellipsis"> <a class="same-property-bottom" href="/pl_p3d71f15e087dc5847a52e54a5bd102f.html">刘春宇</a> </div> </div> </li> <li class="list-group-item clearfix"> <div class="title"> <div class="head"> <img class="usericon partner-letter" src="https://qccdata.qichacha.com/AutoImage/dd96d29d1b2ae487d7c191335984d47b.jpg?x-oss-process=image/resize,w_120" onerror="this.src='https://co-image.qichacha.com/CompanyImage/default.jpg'"> </div> <div class="name same-property-ellipsis"> <a class="same-property-top" href="/firm_dd96d29d1b2ae487d7c191335984d47b.html">江阴市鑫南橡塑制品有限公司</a> </div> <div class="content same-property-ellipsis"> <a class="same-property-bottom" href="/pl_pab76207a22b88e94973f3f5c99c96ad.html">缪仲宪</a> </div> </div> </li> <li class="list-group-item clearfix"> <div class="title"> <div class="head"> <img class="usericon partner-letter" src="https://qccdata.qichacha.com/AutoImage/247d3eae9f7372fd90b6ea3ac7a39028.jpg?x-oss-process=image/resize,w_120" onerror="this.src='https://co-image.qichacha.com/CompanyImage/default.jpg'"> </div> <div class="name same-property-ellipsis"> <a class="same-property-top" href="/firm_247d3eae9f7372fd90b6ea3ac7a39028.html">无锡市诚州橡胶有限公司</a> </div> <div class="content same-property-ellipsis"> <a class="same-property-bottom" href="/pl_p60e95b5e4c429ba835bbd53c10b3af5.html">吴国新</a> </div> </div> </li> <li class="list-group-item clearfix"> <div class="title"> <div class="head"> <img class="usericon partner-letter" src="https://qccdata.qichacha.com/AutoImage/dcf35e8a73af851a362d52e2c96e1589.jpg?x-oss-process=image/resize,w_120" onerror="this.src='https://co-image.qichacha.com/CompanyImage/default.jpg'"> </div> <div class="name same-property-ellipsis"> <a class="same-property-top" href="/firm_dcf35e8a73af851a362d52e2c96e1589.html">宜兴市宏成橡塑制品有限公司</a> </div> <div class="content same-property-ellipsis"> <a class="same-property-bottom" href="/pl_p9ecd67bf926e8e633e7be68d41f2c16.html">史暗生</a> </div> </div> </li> </ul> </section> <div class="m-b"> <a onclick="zhugeTrack('右侧内容点击',{'内容名称':'企查查小程序','企查查小程序来源':'企业主页'});" rel="nofollow" href="https://www.qichacha.com/weixin_xcx" target="_blank"> <img src="https://co-image.qichacha.com/upload/chacha/img/20190319/1552977777156818.png" style="width:280px;" alt="企查查"/> </a> </div> </div> </div> </div> <style>
    #appDownloadModal .modal-dialog{
        width: 360px;
        height: 480px;
    }
    #appDownloadModal .modal-dialog .modal-content{
        width: 360px;
        height: 480px;
    }
    #appDownloadModal .modal-body{
        padding: 40px;
    }
    #appDownloadModal .modal-footer{
        margin-top: 0;
        text-align: left;
    }
    .qocdeBox{
        width: 278px;
        height: 278px;
        padding: 5px;
        border: 1px solid #c7c7c7;
        margin:auto;
    }
    .qocdeBox img{
        width: 100%;
    }
</style> <div class="modal fade" id="appDownloadModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">下载APP</h4> </div> <div class="modal-body"> <div class="qocdeBox"> <img src="/material/theme/chacha/cms/app/images/download_qcode.png" alt="企查查APP下载"/> </div> </div> <div class="modal-footer">
                扫描下载企查查APP，公司股权占比一览无余
            </div> </div> </div> </div> <script type="text/javascript">
if('' == 'export'){
    zhugeTrack('企业主页',{'企业名称':'江苏华兰药用新材料股份有限公司','来源':'数据导出'});
}else{
    zhugeTrack('企业主页',{'企业名称':'江苏华兰药用新材料股份有限公司'});
}

  var ipoTag = false;
 $(function(){
    setCompanyNavFixed();
    getRightNotice('5f981c1538705fe2ec4891565b370edc');
    getRightPromote('5f981c1538705fe2ec4891565b370edc');
    setUnloginJumpFp();
 })  

  setTimeout(function() {
    $('#loginModal').modal('show');
    getCaptcha();
 }, 1000);
 
</script> <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/company-footer.css?time=1497542400" type="text/css"/> <div class="modal fade" id="shareModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-body"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <div class="share"> <h3>分享到</h3> <p>微信扫描二维码分享</p> <div id="qrcode" data=""></div> <a rel="nofollow" href="http://service.weibo.com/share/share.php?title=企业内幕：你所不了解的江苏华兰药用新材料股份有限公司 | 查企业，就上企查查！&amp;url=http://www.qichacha.com/firm_5f981c1538705fe2ec4891565b370edc.html" class="btn btn-lg btn-icon btn-danger btn-rounded btn-inactive m-r-xs m-t" target="_blank"> <i class="fa fa-weibo"></i></a> <a href="mailto:?subject=企业内幕：你所不了解的江苏华兰药用新材料股份有限公司 | 查企业，就上企查查！&amp;body=http://www.qichacha.com/firm_5f981c1538705fe2ec4891565b370edc.html" class="btn btn-lg  btn-icon btn-info btn-rounded btn-inactive m-l m-t" target="_blank"><i class="fa fa-envelope"></i></a> </div> </div> </div> </div> </div> <div class="modal fade" id="groupModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal" style="width: 600px;"> <div class="modal-content"> <div class="modal-header"> <button id="editNewClose" type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">添加关注</h4> </div> <div class="modal-body"> <div class="group-panel"> <ul class="tab clearfix"> <li class="active"> <a href="#groupEdit" data-toggle="tab"> 加入已有分组 </a> </li> <li> <a href="#groupAdd" data-toggle="tab">加入新分组</a> </li> </ul> <div class="tab-content"> <div class="tab-pane fade in active" id="groupEdit"> <div class="edit-wrap"> <table class="table" id="groupList"> </table> </div> </div> <div class="tab-pane fade" id="groupAdd"> <input type="text" class="form-control" placeholder="请输入新分组名称" value=""/> </div> </div> </div> </div> <div class="modal-footer"> <input type="hidden" value="5f981c1538705fe2ec4891565b370edc" id="groupCompanykey"/> <button type="button" onclick="editDone()" class="btn btn-primary">
                    确定
                </button> </div> </div> </div> </div> <div class="modal fade" id="transferFilesModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal nmodal-sm"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">申请工商调档</h4> </div> <div class="modal-body"> <form class="form-horizontal" role="form"> <div class="form-group"> <label class="col-sm-2">手机号码</label> <div class="col-sm-10"> <input type="text" class="form-control transferFilesPhone" placeholder="请输入您的手机号码"> <span class="phonemsg text-danger"></span> </div> </div> <div class="form-group"> <label class="col-sm-2">姓名</label> <div class="col-sm-10"> <input type="text" class="form-control transferFilesName" placeholder="请输入您的真实姓名"> <span class="emailmsg text-danger"></span> </div> </div> <div class="form-group"> <label class="col-sm-2">查档类型</label> <div class="col-sm-10"> <textarea class="form-control transferFilesType" rows="3" placeholder="请输入您要查询的档案类型"></textarea> <span class="text-danger"></span> </div> </div> <div class="form-group m-t-lg"> <label class="col-sm-2">&nbsp;</label> <div class="col-sm-10 text-center"> <input type="hidden" class="transferFilesCompanykey" value="5f981c1538705fe2ec4891565b370edc"/> <span class="btn btn-primary btn-block transferFilesSubmit">提交</span> </div> </div> </form> </div> </div> </div> </div> <div class="modal fade" id="contactModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal nmodal-sm"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">委托联系</h4> </div> <div class="modal-body"> <form class="form-horizontal" role="form" id="contactCompany"> <div id="contactForm" style="height: 530px;"> <div class="form-group"> <label class="col-sm-2">您的姓名</label> <div class="col-sm-10"> <input type="text" class="form-control" name="name" placeholder="请输入您的姓名"> <span msgfor="name"></span> </div> </div> <div class="form-group"> <label class="col-sm-2">手机号</label> <div class="col-sm-10"> <input type="text" class="form-control" name="phone" placeholder="请输入手机号"> <span msgfor="phone"></span> </div> </div> <div class="form-group"> <label class="col-sm-2">邮箱</label> <div class="col-sm-10"> <input type="text" class="form-control" name="email" placeholder="请输入邮箱"> <span msgfor="email"></span> </div> </div> <div class="form-group"> <label class="col-sm-2">公司名称</label> <div class="col-sm-10"> <input type="text" class="form-control" name="companyName" placeholder="请输入公司名称"> <span msgfor="companyName"></span> </div> </div> <div class="form-group"> <label class="col-sm-2">所在行业</label> <div class="col-sm-10"> <input type="text" class="form-control" name="industry" placeholder="请输入所在行业"> <span msgfor="industry"></span> </div> </div> <div class="form-group"> <label class="col-sm-2">职位</label> <div class="col-sm-10"> <input type="text" class="form-control" name="job" placeholder="请输入职位"> <span msgfor="job"></span> </div> </div> <div class="form-group"> <label class="col-sm-2">委托事由</label> <div class="col-sm-10"> <textarea style="resize:none;line-height: 1.2;" class="form-control" rows="4" maxlength="140" name="content" placeholder="请输入委托事由" onChange="checkWord(this);" onKeyUp="checkWord(this);" onMouseDown="checkWord(this);"></textarea> <div id="inputLimit" style="position: absolute;display: none; color: #999;font-size: 12px;right: 14px;"><span>120</span>/140字</div> <span msgfor="content"></span> </div> </div> <div class="m_declare"> <p>重要声明：</p> <p style="line-height: 1.3;">请您如实的填写以上信息，企查查仅对您填写的信息进行形式审查，因您填写的信息虚假、错误等造成的后果，由委托人自行承担，企查查不承担任何责任。委托人填写的委托事由，应当符合国家法律、法规、规章的规定，否则造成的任何后果由委托人自行承担。若因法律、法规的规定由企查查承担责任的，企查查有权向委托人追偿。 </p> </div> </div> <div id="contactPreview" style="display: none;height: 530px;background: url(/material/theme/chacha/cms/v2/images/wtmb.png) no-repeat; background-size: 100%;"> <div class="mbyl-middle"> <div class="title">江苏华兰药用新材料股份有限公司，您好：</div> <div class="subtitle">
                                我是 <span id="ylCompanyName"></span> 的 <span id="ylName"></span>，真诚期待与贵公司合作，以下是我的联系方式，期待您的回复！
                            </div> <div class="tip-contact">行业：<span id="ylIndustry"></span></div> <div class="tip-contact">职位：<span id="ylJob"></span></div> <div class="tip-contact">手机：<span id="ylPhone"></span></div> <div class="tip-contact">邮箱：<span id="ylEmail"></span></div> <div class="tip-contact">委托事由：<span id="ylContent"></span></div> <div class="tip-wrap"> <div class="step-title">重要说明：</div> <div class="step-content">
                                    该邮件是企查查接受平台用户 <span id="ylName2"></span> 的委托，向贵公司发送的系统邮件（请勿直接回复），以帮助企业促成商务合作，邮件内容及信息不代表企查查的任何观点及保证，请自行判断商业风险，企查查不承担任何责任。
                                </div> </div> </div> </div> <div class="form-group m-t-md"> <label class="col-sm-2">&nbsp;</label> <div class="col-sm-10 text-right"> <input type="hidden" name="type" value="2"/> <input type="hidden" name="companykey" value="5f981c1538705fe2ec4891565b370edc"/> <input type="hidden" name="toCompanyName" value="江苏华兰药用新材料股份有限公司"/> <span class="btn btn-primary m-r-sm" id="ylBtn" onclick="contactCompanyPreview();">邮件预览</span> <button type="submit" class="btn btn-primary contactCompany1">委托发送</button> </div> </div> </form> </div> </div> </div> </div> <div class="modal fade" id="postCardModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title postcard-tep1">设置名片</h4> <h4 class="modal-title postcard-tep2">发送名片</h4> </div> <form class="form-horizontal pform" role="form" id="postCardForm"> <div class="modal-body postcard-tep1"> <div class="form-group"> <label class="col-pre">选择头像<span class="redstar">*</span></label> <div class="col-after" style="margin-top: 8px;"> <div id="uploadFaceImgArea" class="fileinput"> <div class="img" onclick="fileinput('faceImg')" style="display: block;"> <img src="" onerror="this.src='/material/theme/chacha/cms/v2/images/default_face.png'"> <span>上传头像</span> </div> <input type="hidden" name="faceimg"> <span class="message" msgfor="faceimg"> </span> </div> </div> </div> <div class="form-group"> <label class="col-pre">真实姓名<span class="redstar">*</span></label> <div class="col-after"> <input type="text" class="form-control" name="name" placeholder="请输入真实姓名" value=""> <span msgfor="name"></span> </div> </div> <div class="form-group"> <label class="col-pre">公司<span class="redstar">*</span></label> <div class="col-after"> <input type="hidden" name="my_company_keyno" id="postCardCompanyKey" value=""> <input type="text" class="form-control" name="my_company_name" id="postCardCompanyName" onclick="scompanyList(this.value,'postCardCompanyList','postCardCompanyName','postCardCompanyKey')" onkeyup="scompanyList(this.value,'postCardCompanyList','postCardCompanyName','postCardCompanyKey')" autocomplete="off" placeholder="请输入所属公司" value=""> <section class="scompany-list" id="postCardCompanyList" style="position: absolute;width: 427px"></section> <span msgfor="my_company_name"></span> </div> </div> <div class="form-group"> <label class="col-pre">职位<span class="redstar">*</span></label> <div class="col-after"> <input type="text" class="form-control" name="position" placeholder="请输入公司职位" value=""> <span msgfor="position"></span> </div> </div> <div class="form-group"> <label class="col-pre">电话<span class="redstar">*</span></label> <div class="col-after"> <input type="hidden" name="phone_prefix" value=""> <input type="text" class="form-control" name="phone" value="" placeholder="请输入联系电话" value=""> <span msgfor="phone"></span> </div> </div> <div class="form-group"> <label class="col-pre">邮箱<span class="redstar">*</span></label> <div class="col-after"> <input type="text" class="form-control" name="email" value="" placeholder="请输入联系邮箱" value=""> <span msgfor="email"></span> </div> </div> <div class="form-group"> <div class="col-all"> <p class="ts">发送的名片将以APP通知或邮件形式送达指定企业，禁止发布广告、骚扰等无关信息。如收到举报并核实，企查查有权永久封禁被举报账号。</p> </div> </div> </div> <div class="modal-body postcard-tep2"> <div class="postcard-wrap"> <div class="pcard-content"> <div class="clearfix"> <div class="col-ft"> <div class="img"> <img id="postcardImg" onerror="this.src='/material/theme/chacha/cms/v2/images/default_face.png'"> </div> </div> <div class="col-bd"> <div class="title"> <h4 id="postcardName">雷军</h4> <span id="postCardCompany">小米科技有限责任公司</span> </div> </div> </div> <div class="clearfix m-t-sm"> <span class="des">职位：</span> <span id="postCardPostion" class="value">CEO</span> </div> <div class="clearfix m-t-xs"> <span class="des">电话：</span> <span id="postCardPhone" class="value">13872119231</span> </div> <div class="clearfix m-t-xs"> <span class="des">邮箱：</span> <span id="postCardEmail" class="value">leijun@xiaomi.com</span> </div> </div> </div> <div class="form-group m-t-md"> <div class="col-all"> <textarea style="resize: none;" rows="3" name="cooperation_intention" class="form-control" placeholder="请输入合作意向，详细介绍你的合作意向，有助于推动对方快速联系你"></textarea> <span msgfor="cooperation_intention"></span> </div> </div> <div class="form-group"> <div class="col-all"> <p class="ts">发送的名片将以APP通知或邮件形式送达指定企业，禁止发布广告、骚扰等无关信息。如收到举报并核实，企查查有权永久封禁被举报账号。</p> </div> </div> </div> <div class="modal-footer"> <input type="hidden" name="to_company_keyno" value="5f981c1538705fe2ec4891565b370edc"> <input type="hidden" name="to_company_email" value="wangjf@hlnpm.com"> <input type="hidden" name="to_company_name" value="江苏华兰药用新材料股份有限公司"> <button type="button" onclick="postcardTep(2)" class="btn btn-primary postcard-tep1">下一步</button> <a rel="nofollow" href="/user_setting?from=f" class="btn btn-default postcard-tep2">修改信息</a> <button type="submit" class="btn btn-primary postcard-tep2">发送名片</button> </div> </form> <form class="pform-uploadimg" enctype="multipart/form-data" id="uploadFaceImg"> <input type="file" id="faceImg" name="pic"> </form> </div> </div> </div> <div class="modal fade" id="toSettingModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm" style="width: 450px;"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">提示</h4> </div> <div class="modal-body"> <div class="pnodata"> <img src="/material/theme/chacha/cms/v2/images/nno_image.png"> <p>投递名片，请确认已绑定手机号、邮箱以及完善个人信息</p> </div> </div> <div class="modal-footer"> <a rel="nofollow" href="/user_setting?from=f" class="btn btn-primary">去设置</a> </div> </div> </div> </div> <div class="modal fade" id="phoneModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal" style="width: 400px"> <div class="modal-content qy-modal"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">更多号码
                
                <span class="ntag vip m-l-sm" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title="尊敬的会员，您正在使用高级特权">功能</span> </h4> </div> <div class="modal-body"> <div class="clearfix font-15 m-b-sm"> <div class="pull-left">0510-68951508</div> <div class="pull-right text-muted">
                                                            2014年报
                                                    </div> </div> </div> </div> </div> </div> <div class="modal fade" id="hisEmailModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal" style="width: 400px"> <div class="modal-content qy-modal"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">更多邮箱</h4> </div> <div class="modal-body"> <div class="clearfix font-15 m-b-sm"> <div class="pull-left">hlnpm@hlnpm.com</div> <div class="pull-right text-muted">
                                                                    2016年报
                                                            </div> </div> <div class="clearfix font-15 m-b-sm"> <div class="pull-left">hualan@hlnpm.com</div> <div class="pull-right text-muted">
                                                                    2015年报
                                                            </div> </div> <div class="clearfix font-15 m-b-sm"> <div class="pull-left">hlnpm@hlnmp.com</div> <div class="pull-right text-muted">
                                                                    其他
                                                            </div> </div> </div> </div> </div> </div> <div class="modal fade" id="companyFeedModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="myModalLabel">意见反馈</h4> </div> <form class="form-horizontal pform" role="form" id="companyFeedForm"> <div class="modal-body"> <div class="form-group"> <label class="col-pre">公司名称</label> <div class="col-after"> <input type="text" class="form-control" name="company_name" readonly="readonly" placeholder="请输入公司职位" value="江苏华兰药用新材料股份有限公司"> <span msgfor="company_name"></span> </div> </div> <div class="form-group"> <label class="col-pre">有误模块<span class="redstar">*</span></label> <div class="col-after"> <input type="hidden" name="category" value=""> <div id="errorCategory"> <a data-value="1" onclick="setErrorCat(this)" class="se-item">工商信息</a> <a data-value="2" onclick="setErrorCat(this)" class="se-item">投资关系</a> <a data-value="3" onclick="setErrorCat(this)" class="se-item">失信信息</a> <a data-value="5" onclick="setErrorCat(this)" class="se-item">被执行人</a> <a data-value="12" onclick="setErrorCat(this)" class="se-item">法院公告</a> <a data-value="4" onclick="setErrorCat(this)" class="se-item">裁判文书</a> <a data-value="13" onclick="setErrorCat(this)" class="se-item">经营异常</a> <a data-value="14" onclick="setErrorCat(this)" class="se-item">行政处罚</a> <a data-value="15" onclick="setErrorCat(this)" class="se-item">环保处罚</a> <a data-value="16" onclick="setErrorCat(this)" class="se-item">动产抵押</a> <a data-value="17" onclick="setErrorCat(this)" class="se-item">土地抵押</a> <a data-value="18" onclick="setErrorCat(this)" class="se-item">开庭公告</a> <a data-value="19" onclick="setErrorCat(this)" class="se-item">司法拍卖</a> <a data-value="20" onclick="setErrorCat(this)" class="se-item">股权冻结</a> <a data-value="21" onclick="setErrorCat(this)" class="se-item">简易注销</a> <a data-value="22" onclick="setErrorCat(this)" class="se-item">公示催告</a> <a data-value="23" onclick="setErrorCat(this)" class="se-item">税收违法</a> <a data-value="24" onclick="setErrorCat(this)" class="se-item">股权出质</a> <a data-value="25" onclick="setErrorCat(this)" class="se-item">送达公告</a> <a data-value="26" onclick="setErrorCat(this)" class="se-item">严重违法</a> <a data-value="27" onclick="setErrorCat(this)" class="se-item">欠税公告</a> <a data-value="6" onclick="setErrorCat(this)" class="se-item">商标</a> <a data-value="7" onclick="setErrorCat(this)" class="se-item">专利</a> <a data-value="8" onclick="setErrorCat(this)" class="se-item">著作权</a> <a data-value="9" onclick="setErrorCat(this)" class="se-item">企业证书</a> <a data-value="10" onclick="setErrorCat(this)" class="se-item">变更记录</a> <a data-value="11" onclick="setErrorCat(this)" class="se-item">其他</a> </div> <span msgfor="category"></span> </div> </div> <div class="form-group"> <label class="col-pre">补充说明<span class="redstar">*</span></label> <div class="col-after"> <textarea rows="4" name="content" class="form-control" placeholder="感谢您帮我们发现了不足之处，请留下您的宝贵意见。"></textarea> <span msgfor="content"></span> </div> </div> <div class="form-group"> <label class="col-pre">图片附件<div style="font-size: 12px;color: #999;line-height: 1">（选填）</div></label> <div class="col-after" style="margin-top: 8px;"> <div id="uploadVisitPicArea" class="fileinput"> <span class="noimg"> <a class="btn" onclick="fileinput('addVisitPic')" href="javascript:;">选择文件</a> <span>未选择文件</span> </span> <div class="img" onclick="fileinput('addVisitPic')"> <img src="" onerror="this.src='/material/theme/chacha/cms/v2/images/no_image.png'"> <span>修改图片</span> </div> <input type="hidden" name="imageurl"> <span class="message" msgfor="imageurl" style="margin-top: -36px;margin-left: 20px;"> </span> </div> <span class="ts">仅支持jpg、jpeg、png格式，大小不超过5M</span> </div> </div> <div class="form-group"> <label class="col-pre">手机号<span class="redstar">*</span></label> <div class="col-after"> <input type="text" class="form-control" name="phone" value="" placeholder="请输入联系邮箱" value=""> <span msgfor="phone"></span> </div> </div> </div> <div class="modal-footer"> <input type="hidden" name="company_keyno" value="5f981c1538705fe2ec4891565b370edc"> <button type="submit" class="btn btn-primary">提交</button> </div> </form> <form class="pform-uploadimg" enctype="multipart/form-data" id="uploadVisitAddPic"> <input type="file" id="addVisitPic" name="pic"> </form> </div> </div> </div> <div class="modal fade" id="radarTsModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">提示</h4> </div> <div class="modal-body"> <p class="m-b-lg">您的监控企业数量已达上限（100家），升级SVIP会员最多可监控500家企业。</p> </div> <div class="modal-footer"> <a rel="nofollow" href="/vip_svip" class="btn btn-primary pull-right">立即开通</a> </div> </div> </div> </div> <div class="modal fade" id="editContactInfoModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">编辑企业信息</h4> </div> <div class="modal-body"> <div class="m-b-lg ct">完成企业认证后，即可拥有修改企业联系方式，接收合作名片、发布企业官方公告等多项企业服务。
                    <a rel="nofollow" class="text-primary demotd" target="_blank" href="https://pinpai.qichacha.com/own_f625a5b661058ba5082ca508f99ffe1b.html">查看样例> </a> <div class="m-t-md text-center"> <img style="width: 412px;" src="/material/theme/chacha/cms/v2/images/promote102.png" alt="企业认证"> </div> </div> </div> <div class="modal-footer"> <a onclick="zhugeTrack('企业主页-编辑电话-认证企业',{'对象类型':'认证本企业'});" rel="nofollow" href="/company_cert?companykey=5f981c1538705fe2ec4891565b370edc&companyname=%E6%B1%9F%E8%8B%8F%E5%8D%8E%E5%85%B0%E8%8D%AF%E7%94%A8%E6%96%B0%E6%9D%90%E6%96%99%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8" class="btn btn-primary pull-right">认证本企业</a> <a onclick="zhugeTrack('企业主页-编辑电话-认证企业',{'对象类型':'认证自己企业'});" rel="nofollow" href="/company_cert" class="btn btn-default pull-right m-r-sm">认证自己企业</a> </div> </div> </div> </div> <div class="modal fade" id="websiteCertModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">网络安全认证</h4> </div> <div class="modal-body"> <div class="m-b-lg ct">完成联合认证后，即可获得超级认证的全部服务，以及在企查查、QQ聊天窗口、搜狗浏览器、QQ浏览器等平台绿V展示，提升用户对企业的信任，彰显企业实力。
                    <a rel="nofollow" class="text-primary demotd" target="_blank" href="/more_certunite">详情></a> <div class="m-t-md text-center"> <img style="width: 412px;" src="/material/theme/chacha/cms/v2/images/promote101.png" alt="企业认证"> </div> </div> </div> <div class="modal-footer"> <a rel="nofollow" href="/company_certunite?companykey=5f981c1538705fe2ec4891565b370edc&companyname=%E6%B1%9F%E8%8B%8F%E5%8D%8E%E5%85%B0%E8%8D%AF%E7%94%A8%E6%96%B0%E6%9D%90%E6%96%99%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8" class="btn btn-primary pull-right">认证本企业</a> <a rel="nofollow" href="/company_certunite" class="btn btn-default pull-right m-r-sm">认证自己企业</a> </div> </div> </div> </div> <div class="modal fade" id="gdczModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">股东出资详情</h4> </div> <div class="modal-body"> <div id="gdczview"></div> </div> </div> </div> </div> <div class="modal fade" id="zhixingModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="zhixingModalLabel">被执行人详情</h4> </div> <div class="modal-body"> <div id="zhixingview"></div> </div> </div> </div> </div> <div class="modal fade" id="shixinModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="shixinModalLabel">失信被执行人详情</h4> </div> <div class="modal-body"> <div id="shixinview"></div> </div> </div> </div> </div> <div class="modal fade" id="ktnoticeModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="ktnoticeModalLabel">开庭公告详情</h4> </div> <div class="modal-body"> <div id="ktggview"></div> </div> </div> </div> </div> <div class="modal fade" id="wenModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="wenModalModalLabel">裁判文书详情</h4> </div> <div class="modal-body"> <div id="wsview"></div> </div> </div> </div> </div> <div class="modal fade" id="otherPunishModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">行政处罚详情[其他]</h4> </div> <div class="modal-body"></div> </div> </div> </div> <div class="modal fade" id="assistanceModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="myModalLabel">股权冻结详情</h4> </div> <div class="modal-body"> <div id="xzxkview"></div> </div> </div> </div> </div> <div class="modal fade" id="gonggaoModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="gonggaoModalLabel">法院公告详情</h4> </div> <div class="modal-body"> <div id="gonggaoview"></div> </div> </div> </div> </div> <div class="modal fade" id="zzqModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="zzqModalModalLabel">著作权详情</h4> </div> <div class="modal-body"> <div class="zzqview"></div> <div class="clearfix"></div> </div> </div> </div> </div> <div class="modal fade" id="mPledgeModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">动产抵押详情</h4> </div> <div class="modal-body" style="max-height: calc(100vh - 125px);overflow-y: auto;"> <div id="mPledgeview"></div> </div> </div> </div> </div> <div class="modal fade" id="stockModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal relat-modal"> <div class="modal-content relat-modal-list"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="stockModalTitle">持股详情</h4> </div> <div class="modal-body" id="stockdetail"> </div> </div> <div class="modal-content relat-modal-detail"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <a href="javascript:;" class="fa fa-chevron-left" onclick="backRelatList()"></a> <h4 class="modal-title">详情</h4> </div> <div class="modal-body" id="stockrelate"> </div> </div> </div> </div> <div class="modal fade" id="benefitModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="stockModalTitle">股权链</h4> </div> <div class="modal-body" id="benefitdetail"> </div> </div> </div> </div> <div class="modal fade" id="investListModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">对外投资</h4> </div> <div class="modal-body" style="max-height: calc(100vh - 125px);overflow-y: auto;"> </div> </div> </div> </div> <div class="modal fade" id="guquanListModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">股权结构</h4> </div> <div class="modal-body" style="max-height: calc(100vh - 125px);overflow-y: auto;"> </div> </div> </div> </div> <div class="modal fade" id="relatedListModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title"><span class="t">关联企业</span><span class="ntag vip m-l-sm" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title="尊敬的会员，您正在使用高级特权">功能</span></h4> </div> <div class="modal-body" style="max-height: calc(100vh - 125px);overflow-y: auto;"> </div> </div> </div> </div> <div class="modal fade" id="pledgeModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">股权出质详情</h4> </div> <div class="modal-body"> <div id="pledgeview"></div> </div> </div> </div> </div> <div class="modal fade" id="spledgeModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">质押明细</h4> </div> <div class="modal-body"> </div> </div> </div> </div> <div class="modal fade" id="cfModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="myModalLabel">行政处罚详情</h4> </div> <div class="modal-body"> <div class="xzcfview"></div> <div class="clearfix"></div> </div> </div> </div> </div> <div class="modal fade" id="zhuxiaoModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">简易注销</h4> </div> <div class="modal-body"> <table class="ntable" id="flowlist"> <tr> <td class="tb" width="20%" rowspan="5">企业公告信息</td> <td>企业名称</td> <td>-</td> </tr> <tr> <td>统一社会信用代码/注册号</td> <td>-</td> </tr> <tr> <td>登记机关</td> <td>-</td> </tr> <tr> <td>公告期</td> <td>-</td> </tr> <tr> <td>全体投资人承诺书</td> <td>
                            -                        </td> </tr> <tr> <td class="tb" width="20%" rowspan="3">异议信息</td> <td>异议申请人</td> <td>-</td> </tr> <tr> <td>异议时间</td> <td>-</td> </tr> <tr> <td>异议内容</td> <td>-</td> </tr> <tr> <td class="tb" width="20%" rowspan="3">简易注销结果</td> <td>简易注销结果</td> <td>-</td> </tr> <tr> <td>公告申请日期</td> <td>-</td> </tr> </table> </div> </div> </div> </div> <div class="modal fade" id="noteModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">写笔记</h4> </div> <div class="modal-body"> <form class="form-horizontal" role="form"> <div class="form-group"> <div class="col-sm-12"> <textarea class="form-control noteContent" style="resize: vertical" rows="5" placeholder="亲爱的用户：请在这里填写您对该企业的笔记"></textarea> <span class="contentmsg text-danger"></span> </div> </div> <div class="form-group m-t-lg"> <div class="col-sm-12 text-center"> <input type="hidden" class="noteCompanykey" value="5f981c1538705fe2ec4891565b370edc"/> <input type="hidden" class="noteCompanyname" value="江苏华兰药用新材料股份有限公司"/> <span class="btn btn-primary noteSubmit btn-block">提交</span> </div> </div> </form> </div> </div> </div> </div> <div class="modal fade" id="gdPledgeModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">股权出质详情</h4> </div> <div class="modal-body" style="max-height: calc(100vh - 125px);overflow-y: auto;"> </div> </div> </div> </div> <div class="modal fade" id="gdAssistanceModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">股权冻结详情</h4> </div> <div class="modal-body" style="max-height: calc(100vh - 125px);overflow-y: auto;"> </div> </div> </div> </div> <div class="modal fade" id="note2Modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal" style="width: 600px;"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">笔记</h4> </div> <div class="modal-body" style="padding: 20px;"> <div id="nNodeList" class="nnote-list"> </div> <div class="form-horizontal" role="form"> <div class="form-group"> <div class="col-sm-12"> <textarea class="form-control" id="nNoteContent" style="resize: none;" rows="5" placeholder="亲爱的用户：请在这里填写您对该企业的笔记"></textarea> <span class="contentmsg text-danger"></span> <input type="hidden" id="nNoteId" value=""/> </div> </div> </div> <div class="clearfix m-t-md m-b-sm"> <button onclick="noteSave('5f981c1538705fe2ec4891565b370edc','江苏华兰药用新材料股份有限公司',this)" style="width: 82px;outline: none;" class="btn btn-primary pull-right">提交</button> </div> </div> </div> </div> </div> <div class="modal fade" id="reportModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal report-modal"> <div class="modal-content "> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">下载报告
                                        <a rel="nofollow" target="_blank" class="text-primary font-14" style="font-weight: normal;" href="/vip">成为VIP免费下载本页所有报告，立即开通></a> </h4> </div> <div class="modal-body"> </div> </div> </div> </div> <div class="modal fade" id="savefpModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm savefp-modal" style="top: 100px;"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title postcard-tep1">保存发票抬头</h4> </div> <div class="modal-body clearfix"> <div class="tax-view" id="taxView"> <p class="clearfix"><span class="des">企业名称：</span><span class="Name">暂无</span></p> <p class="clearfix"><span class="des">企业税号：</span><span class="CreditCode">暂无</span></p> <p class="clearfix"><span class="des">企业地址：</span><span class="Address">暂无</span></p> <p class="clearfix"><span class="des">企业电话：</span><span class="PhoneNumber">暂无</span></p> <p class="clearfix"><span class="des">开户银行：</span><span class="Bank">暂无</span></p> <p class="clearfix"><span class="des">银行账户：</span><span class="Bankaccount">暂无</span></p> </div> <div class="qrcode-view"> <div class="tab"> <a onclick="qrcodeViewTab(this,1,'5f981c1538705fe2ec4891565b370edc')" class="active">APP扫码</a> <a onclick="qrcodeViewTab(this,2,'5f981c1538705fe2ec4891565b370edc')">微信扫码</a> </div> <div class="qrcodewrap" id="qrcodeViewApp"> <div class="qrcode" id="qrcodeViewAppCode"></div> <div class="imgts"> <p>企查查APP扫描二维码</p> <p class="text-gray">在首页-发票抬头查看</p> <img src="/material/theme/chacha/cms/v2/images/qrcodeViewAppImg.png"> </div> <p><a rel="nofollow" href="/app" class="text-primary" target="_blank">企查查APP</a> 扫一扫保存发票抬头</p> </div> <div class="qrcodewrap" id="qrcodeViewWx" style="position: relative;display: none;"> <div class="qrcode" id="qrcodeViewWxCode"> <img class="loadimg" src="/material/theme/chacha/cms/v2/images/preloader.gif"> </div> <div class="imgts"> <p>微信扫描二维码</p> <p class="text-gray">关注公众号在-发票抬头中可查看</p> <img src="/material/theme/chacha/cms/v2/images/qrcodeViewWxImg.png"> </div> <p>微信 扫一扫保存发票抬头</p> </div> </div> </div> </div> </div> </div> <input type="hidden" id="provice" name="provice" value=""> <input type="hidden" id="unique" name="unique" value="5f981c1538705fe2ec4891565b370edc"> <input type="hidden" id="companyname" value="江苏华兰药用新材料股份有限公司"> <input type="hidden" id="companyid" name="companyid" value=""> <input type="hidden" id="brandcount" name="brandcount" value=""> <input type="hidden" id="companylogo" value=""> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/jquery.scrollTo.min.js"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/browser.js"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/jquery.scrollTo.js"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/echarts.min.v4.js?version=1573121164"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/echarts-wordcloud.min.v4.js"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/china.v4.js"></script> <script src="/material/theme/chacha/cms/v2/js/d3.min.js"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/company.js?version=1573121164"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/modalview.js?version=1573121164"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/companyChart.js?version=1573121164"></script> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/qa.js?version=1573121164"></script> <div class="modal fade" id="hasCertModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal ts-modal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="opercor ModalModalLabel">认证详情</h4> </div> <div class="modal-body clearfix"> <div class="title font-16 clearfix"> <div class="bd"> <span class="icon-infos"></span> </div> <div class="bd" style="padding-left: 10px;"> <span>您已提交本企业的认证资料，请前往个人中心查看认证结果</span> </div> </div> <div class="btn-area m-t-md pull-right"> <a rel="nofollow" class="btn btn-primary m-r-xs" href="/user_company">立即前往</a> </div> </div> </div> </div> </div> <div class="modal fade" id="opercorModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal" style="width: 1170px"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="opercor ModalModalLabel">人物图谱</h4> </div> <div class="modal-body n-p"> <div id="opercorview"> </div> </div> </div> </div> </div> <div class="modal fade" id="guquanModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal" style="width: 1170px"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">股权结构图<span class="ntag vip m-l-sm" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title="尊敬的会员，您正在使用高级特权">功能</span></h4> </div> <div class="modal-body n-p"> <div style="height: 641px;" id="guquanview"></div> </div> </div> </div> </div> <div class="modal fade" id="guquanListModal2" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal" style="width: 1170px"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title"><span class="t">股权结构</span> <span class="ntag vip m-l-sm" data-trigger="hover" data-html="true" data-toggle="tooltip" data-placement="bottom" data-delay="500" title="尊敬的会员，您正在使用高级特权">功能</span> </h4> </div> <div class="modal-body n-p"> <div style="height: 641px;" id="guquanlist"></div> </div> </div> </div> </div> <div class="modal fade" id="investAgencyModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal" style="width: 1170px"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="investAgencyModalLabel">投资机构</h4> </div> <div class="modal-body"> <table class="ntable"> <tr> <th>序号</th> <th>机构图片</th> <th>投资机构</th> <th>城市</th> <th>简介</th> </tr> </table> </div> </div> </div> </div> <div class="modal fade in" tabindex="-1" id="recomendAppModal" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal" style="width: 650px;margin-top: 56px;"> <div class="modal-content"> <a rel="nofollow" class="recomend-app" href="/app"> <button type="button" class="close" style="color: #fff;" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> </a> </div> </div> </div> <div class="modal fade" id="contentDetailModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">行政处罚内容详情</h4> </div> <div class="modal-body"> </div> </div> </div> </div> <div class="modal fade" id="bmqualificationModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">资质详情</h4> </div> <div class="modal-body"> </div> </div> </div> </div> <div class="modal fade" id="bmpersonModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">人员详情</h4> </div> <div class="modal-body" style="max-height: calc(100vh - 125px);overflow-y: auto;"> </div> </div> </div> </div> <div class="modal fade" id="bmprojectModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">项目详情</h4> </div> <div class="modal-body" style="max-height: calc(100vh - 125px);overflow-y: auto;"> </div> </div> </div> </div> <div class="modal fade" id="RelatModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal relat-modal"> <div class="modal-content relat-modal-list"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">被执行人详情</h4> </div> <div class="modal-body"> <section class="clear"> <div id="relatList"></div> </section> </div> </div> <div class="modal-content relat-modal-detail"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <a href="javascript:;" class="fa fa-chevron-left" onclick="backRelatList()"></a> <h4 class="modal-title"> 被执行人详情</h4> </div> <div class="modal-body"> <section class="clear"> <div class="tcaption">关联失信被执行人</div> <div id="relatDetail"> </div> </section> </div> </div> </div> </div> <script type="text/javascript">

</script> <style type="text/css">
#allmap {width: 100%;height: 600px;}
#mapPreview:hover{cursor:pointer;}
#mapModal .modal-dialog{
    width: 960px;
    margin: 30px auto;
}
</style> <script type="text/javascript" src="https://api.map.baidu.com/api?v=2.0&ak=U0QGae7viQsN0yLBirGsRD90XI0tlcGO&s=1"></script> <div class="modal fade" id="mapModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal lg"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="myModalLabel">完整地图</h4> </div> <div class="modal-body"> <div id="allmap"></div> </div> </div> </div> </div> <script type="text/javascript">
  var isLoadMap;
  // loadScript()
  function showMapModal(address,city,lat,lng){
      $('#mapModal').modal('show');
      if(isLoadMap != address){
          loadmap(address,city);
          isLoadMap = address;
      }
  }


  function loadScript() {  
      var script = document.createElement("script");  
      script.src = "https://api.map.baidu.com/getscript?v=2.0&ak=jYNU39RZ3k37NUz1QduizaYD&services=&t=20171014112628";  
      document.body.appendChild(script);  
  }  


  function loadmap (address,city,lat,lng) {
      /*弹窗大地图*/
      var map = new BMap.Map("allmap");
      map.addControl(new BMap.NavigationControl());
      map.addControl(new BMap.MapTypeControl());
      map.addControl(new BMap.OverviewMapControl());
      map.enableScrollWheelZoom(true);
      // 创建地址解析器实例
      var gc = new BMap.Geocoder();

      //$.colorbox({inline:true, href:"#baiduMap",title:"公司地址"});
      //var address = "江阴市临港新城申港镇澄路1488号";
      map.setCurrentCity(city);
      map.setZoom(12);
      
      gc.getPoint(address, function(point){
          if (point) {
              var p = new BMap.Point(point.lng, point.lat);
              var marker = new BMap.Marker(p);  // 创建标注
              map.addOverlay(marker);              // 将标注添加到地图中
              setTimeout(function(){
                  map.centerAndZoom(p, 15);
              },800);
              map.setZoom(14);
              if(address.length>16){
                address = address.substr(0,15)+'…';
              }
              var sContent =
                      "<h4 style='margin:0 0 5px 0;padding:0.2em 0'>"+city+"</h4>" +
                      "<p style='margin:0;line-height:1.5;font-size:13px;text-indent:0em'>"+address+"</p>" +
                      "</div>";
              var infoWindow = new BMap.InfoWindow(sContent);  // 创建信息窗口对象
              //图片加载完毕重绘infowindow
              marker.openInfoWindow(infoWindow);
          }else{
              faldia({'content':'无法在地图上找到该公司地址'});
          }
      }, city);
  }
</script> <div class="modal fade" id="questionModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal" style="width: 600px;"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">企业问答</h4> </div> <div class="modal-body"> <p style="margin-top: -5px;">您的问题将推荐给2000+用户，TA们将为您解答</p> <div class="textarea-count"> <textarea minlength="4" maxlength="100" class="form-control m-b-lg" style="resize: none;" rows="5"  name="question" 
                    placeholder="写下你的问题，准确的描述问题更容易得到解答"></textarea> <span class="wordwrap"><span class="wordCount">0</span>/<span class="maxCount">100</span></span> </div> </div> <div class="modal-footer"> <input type="hidden" name="keyno" value="5f981c1538705fe2ec4891565b370edc"/> <button type="button" data-dismiss="modal" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()" class="btn btn-primary">发布问题</button> </div> </div> </div> </div> <div class="modal fade" id="answerModal" data-tab="" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm answer-modal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">企业问答</h4> </div> <div class="modal-body"> <span class="icon"></span> <div class="title">雷军给母校武汉大学的最大一笔捐赠为什么是9999.9999万元?</div> <div class="textarea-count"> <textarea minlength="4" maxlength="500" class="form-control" style="resize: none;" rows="5"  name="question" 
                    placeholder="说说你的看法"></textarea> <span class="wordwrap"><span class="wordCount">0</span>/<span class="maxCount">500</span></span> </div> <p class="official-p m-t-xs">您是该企业认证管理员，您提交的回答将作为企业官方回答展示</p> <div class="clearfix m-b-lg"></div> </div> <div class="modal-footer"> <input type="hidden" name="questionId" value=""/> <button type="button" data-dismiss="modal" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()" class="btn btn-primary">回答</button> </div> </div> </div> </div> <div class="modal fade" id="answerListModal" data-tab="" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal" style="width: 900px;"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">共<span class="answer-count"></span>个回答</h4> </div> <div class="modal-body answers"> </div> <div class="modal-footer answer-footer clearfix"> <input type="hidden" name="questionId" value=""/> <label class="pull-left">写回答： <input type="text" minlength="4" maxlength="500" name="content" class="form-control" value="" placeholder="说说看你的想法"></label> <button type="button" data-dismiss="modal" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();zhugeTrack('问答模块按钮点击',{'按钮名称':'回答按钮'});" class="btn btn-primary pull-right">回答</button> </div> </div> </div> </div> <div class="modal fade" id="indictModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">举报</h4> </div> <div class="modal-body"> <p class="font-16">举报原因（可多选）</p> <div class="check-wrap"> <label class="checkbox-inline"> <input type="checkbox" name="reason" value="低俗色情"> 低俗色情
                    </label> <label class="checkbox-inline"> <input type="checkbox" name="reason" value="涉嫌违法犯罪"> 涉嫌违法犯罪
                    </label> <label class="checkbox-inline"> <input type="checkbox" name="reason" value="涉嫌侵权"> 涉嫌侵权
                    </label> <label class="checkbox-inline"> <input type="checkbox" name="reason" value="垃圾广告信息"> 垃圾广告信息
                    </label> <label class="checkbox-inline"> <input type="checkbox" name="reason" value="内容不实"> 内容不实
                    </label> <label class="checkbox-inline"> <input type="checkbox" name="reason" value="人身攻击"> 人身攻击
                    </label> </div> <p class="font-16 m-t">举报详细说明</p> <textarea minlength="4" maxlength="100" class="form-control m-b-lg" style="resize: none;" rows="5"  name="desc" 
                placeholder="请详细说明您要举报的内容（选填）"></textarea> </div> <div class="modal-footer"> <input type="hidden" name="questionId" value=""/> <input type="hidden" name="answerId" value=""/> <button type="button" onclick="indictQA(2)" class="btn btn-primary">完成</button> </div> </div> </div> </div> <div class="modal fade" id="qa404Modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">提示</h4> </div> <div class="modal-body"> <div class="pnodata md"> <img src="/material/theme/chacha/cms/v2/images/nno_image.png"> <p>问题已被删除</p> </div> </div> </div> </div> </div> <script type="text/javascript">
    statInputNum($('#questionModal .textarea-count'),100);
    statInputNum($('#answerModal .textarea-count'),500);
</script> <script type="text/javascript">
    //$('#editContactInfoModal').modal('show');
    function checkWord(dom){
        $('#inputLimit').show();
        $('#inputLimit>span').text(dom.value.length);
    }

    function deputeLoad(iframe){
        var html = iframe.contentWindow.document.getElementsByTagName('html')[0];
        $(html).css('transform-origin','0% 0%');
        $(html).css('transform','scale(0.55)');
        $(html).css('-ms-transform-origin','0% 0%');
        $(html).css('-ms-transform','scale(0.55)');
        $(html).css('-webkit-transform-origin','0% 0%');
        $(html).css('-webkit-transform','scale(0.55)');
        $(html).css('-moz-transform-origin','0% 0%');
        $(html).css('-moz-transform','scale(0.55)');
    }

</script> <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/footer.css?time=1573121164" type="text/css"/> <link rel="stylesheet" href="/material/theme/chacha/cms/v2/css/animate.css?time=1508428800" type="text/css"/> <footer class="footer"> <div class="container"> <div class="footer-top clearfix"> <div class="about" style=""> <h4>关于我们</h4> <ul class="list-unstyled"> <li><a rel="nofollow" onclick="zhugeTrack('底部',{'关于我们':'联系我们'});" href="/cms?id=13">联系我们</a></li> <li><a rel="nofollow" onclick="zhugeTrack('底部',{'关于我们':'用户协议'});" href="/cms?id=14">用户协议</a></li> <li><a rel="nofollow" onclick="zhugeTrack('底部',{'关于我们':'用户隐私权'});" href="/cms?id=15">用户隐私权</a></li> <li><a onclick="zhugeTrack('底部',{'关于我们':'友情链接'});" href="/cms?id=16">友情链接</a></li> <li><a rel="nofollow" onclick="zhugeTrack('底部',{'关于我们':'关于我们'});" href="/cms?id=892">关于我们</a></li> <li><a rel="nofollow" onclick="zhugeTrack('底部',{'关于我们':'用户帮助'});" href="/cms?id=14578">用户帮助</a></li> <li><a rel="nofollow" onclick="zhugeTrack('底部',{'关于我们':'名词百科'});" href="/cms?id=146498">名词百科</a></li> <li><a rel="nofollow" onclick="zhugeTrack('底部',{'关于我们':'产品标签'});" href="/cms?id=146499">产品标签</a></li> <li><a rel="nofollow" onclick="zhugeTrack('底部',{'关于我们':'安全问题反馈'});" href="/cms?id=146516">安全问题反馈</a></li> </ul> </div> <div class="contact"> <h4>联系方式</h4> <ul class="list-unstyled"> <li>企查查官方客服：400-928-2212</li> <li>工作时间: 周一至周五 9:00-20:00</li> <script type="text/javascript" src="/material/js/jquery.cookie.js"></script> <script type="text/javascript" src="/material/js/jquery.validate.min.js"></script> <script type="text/javascript" src="/material/js/jquery.form.min.js"></script> <script type="text/javascript" src="/material/js/global.js?t=1573121164"></script> <li>在线客服：<a data-toggle="modal" data-target="#loginModal" onclick="getCaptcha();">点击在线咨询</a></li> <li>客服邮箱：<a href="mailto:kf@qichacha.com" >kf@qichacha.com</a></li> <li>微信公众号：qcc365</li> <li>地址：江苏省苏州市工业园区东长路88号2.5产业园C1幢5楼</li> </ul> </div> <div class="service" style=""> <h4>查查服务</h4> <ul class="list-unstyled"> <li> <a rel="nofollow" onclick="zhugeTrack('底部',{'查查服务':'企业问答'});" href="https://www.qichacha.com/more_hotqa" target="_blank">企业问答</a> <a onclick="zhugeTrack('底部',{'查查服务':'500强企业'});" href="https://www.qichacha.com/cms_top500" target="_blank">500强企业</a> <a onclick="zhugeTrack('底部',{'查查服务':'疫苗查查'});" href="http://ai.qichacha.com/" target="_blank">疫苗查查</a> <a onclick="zhugeTrack('底部',{'查查服务':'融资查询'});" href="https://www.qichacha.com/elib_financing" target="_blank">融资查询</a> <a onclick="zhugeTrack('底部',{'查查服务':'企业风控'});" href="http://pro.qichacha.com/?source=websiteFoot" target="_blank">企业风控</a> <a onclick="zhugeTrack('底部',{'查查服务':'企业库'});" href="http://www.qichacha.com/elib" target="_blank">企业库</a> <a onclick="zhugeTrack('底部',{'查查服务':'裁判文书查询'});" href="http://www.qichacha.com/more_wenshus" target="_blank">裁判文书查询</a> <a onclick="zhugeTrack('底部',{'查查服务':'新三板企业查询'});" href="http://sanban.qichacha.com" target="_blank">新三板企业查询</a> <a onclick="zhugeTrack('底部',{'查查服务':'上市企业查询'});" href="http://ipo.qichacha.com/" target="_blank">上市企业查询</a> <a onclick="zhugeTrack('底部',{'查查服务':'企查查企业查询'});" href="https://www.qichacha.com/gongsi" target="_blank">企查查企业查询</a> <a onclick="zhugeTrack('底部',{'查查服务':'企查查移动版'});" href="https://m.qichacha.com" target="_blank">企查查移动版</a> <a onclick="zhugeTrack('底部',{'查查服务':'企查查社区'});" href="https://www.qichacha.com/dianping" target="_blank">企查查社区</a> <a onclick="zhugeTrack('底部',{'查查服务':'企业风险搜索'});" href="https://www.qichacha.com/more_shixins" target="_blank">企业风险搜索</a> <a onclick="zhugeTrack('底部',{'查查服务':'商标专利搜索'});" href="https://www.qichacha.com/more_brands" target="_blank">商标专利搜索</a> <a onclick="zhugeTrack('底部',{'查查服务':'企业网址导航'});" href="https://www.qichacha.com/daohang" target="_blank">企业网址导航</a> <a onclick="zhugeTrack('底部',{'查查服务':'企业高管查询'});" href="https://www.qichacha.com/boss" target="_blank">企业高管查询</a> <a onclick="zhugeTrack('底部',{'查查服务':'企业税号查询'});" href="https://www.qichacha.com/tax" target="_blank">企业税号查询</a> <a onclick="zhugeTrack('底部',{'查查服务':'企业新闻头条'});" href="https://www.qichacha.com/news" target="_blank">企业新闻头条</a> <a rel="nofollow" onclick="zhugeTrack('底部',{'查查服务':'企查查下载'});" href="https://www.qichacha.com/weixin" target="_blank">企查查下载</a> <a onclick="zhugeTrack('底部',{'查查服务':'企业失信查询'});" href="https://www.qichacha.com/more_shixins" target="_blank">企业失信查询</a> <a rel="nofollow" onclick="zhugeTrack('底部',{'查查服务':'企查查接口平台'});" href="http://openapi.qichacha.com/?source=websiteFoot" target="_blank">企查查接口平台</a> <a href="/yellowpage" onclick="zhugeTrack('底部',{'查查服务':'公司黄页'});">公司黄页</a> <a href="/cms_dirhot" onclick="zhugeTrack('底部',{'查查服务':'人员名录'});">人员名录</a> <a href="/cms_newlist" onclick="zhugeTrack('底部',{'查查服务':'企业名录'});">企业名录</a> <a rel="nofollow" href="http://open.qichacha.com" onclick="zhugeTrack('底部',{'查查服务':'开放平台'});"target="_blank"> 开放平台</a> </li> </ul> </div> <div class="qrcode"> <div class="qrcode-item"> <img src="/material/theme/chacha/cms/v2/images/v3/code_xcx.png?t=3" alt="企查查APP下载"> <span class="ma_xcx">小程序</span> </div> <div class="qrcode-item"> <img src="/material/theme/chacha/cms/v2/images/v3/code_app.png?t=3" alt="企查查APP下载"> <span class="ma_app">扫码下载APP</span> </div> <div class="qrcode-item"> <img src="/material/theme/chacha/cms/v2/images/v3/code_wx.png?t=3" alt="企查查微信公众号"> <span class="ma_wx">微信公众号</span> </div> </div> </div> <div class="footer-link"> <div class="footer-row clearfix"> <div class="footer-row-head">
                    数据来源：
                </div> <div class="footer-row-content"> <span class="item">全国企业信用信息公示系统</span> <span class="item">中国裁判文书网</span> <span class="item">中国执行信息公开网</span> <span class="item">国家知识产权局</span> <span class="item">商标局</span> <span class="item">版权局</span> </div> </div> </div> </div> <div class="footer-copy-bg"> <div class="container"> <div class="footer-copy clearfix"> <div class="pull-left"> <div class="m-t-xs font-13"> <a href="javascript:void(0)" title="企查查">&copy;2014-2019</a> <a href="http://www.beian.miit.gov.cn/" rel="nofollow" target="_blank"> 苏ICP备15042526号-4</a>
                        版权所有&nbsp;苏州朗动网络科技有限公司
                        &nbsp;增值电信业务经营许可证：<a href="http://www.beian.miit.gov.cn/" rel="nofollow" target="_blank">苏ICP证B2-20180251</a>
                        &nbsp;企业征信备案号：<a href="http://nanjing.pbc.gov.cn/nanjing/117542/117601/117604/3862817/index.html" rel="nofollow" target="_blank">04005</a> <br>
                        违法和不良信息举报电话：400-928-2212&nbsp;&nbsp;举报邮箱：<a href="mailto:jubao@qichacha.com">jubao@qichacha.com</a> </div> </div> <div class="auth"> <a style="margin-left: 0px;" href="https://ss.knet.cn/verifyseal.dll?sn=e17091132050068868mhtm000000&comefrom=trust" rel="nofollow" target="_blank"> <img class="m-l-sm" style="width: 98px" src="/material/theme/chacha/cms/v2/images/dependable.png"/> </a> <a href="http://www.jsdsgsxt.gov.cn/mbm/entweb/elec/certView.shtml?siteId=2f2c5b85a5154355a56eb3dee98ad8a3" rel="nofollow" target="_blank"> <img class="m-l-sm" style="width: 30px" src="/material/theme/chacha/cms/v2/images/jsdsgsxt.png"/> </a> <a href="https://v.yunaq.com/certificate?domain=www.qichacha.com" rel="nofollow" target="_blank"> <img class="m-l-sm" style="width: 106px;" src="/material/theme/chacha/cms/v2/images/gw_124x47.png"/> </a> </div> </div> </div> </div> </footer> <div class="modal fade" id="feedModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title" id="myModalLabel">意见反馈</h4> </div> <form class="form-horizontal pform" role="form"> <div class="modal-body"> <div class="form-group"> <label class="col-pre">问题类别<span class="redstar">*</span></label> <div class="col-after"> <input type="hidden" class="category" name="category" value=""> <div id="indexErrorCategory"> <a data-value="1" onclick="setIndexErrorCat(this)" class="se-item">功能改进</a> <a data-value="2" onclick="setIndexErrorCat(this)" class="se-item">数据问题</a> <a data-value="3" onclick="setIndexErrorCat(this)" class="se-item">搜索问题</a> <a data-value="4" onclick="setIndexErrorCat(this)" class="se-item">投诉反馈</a> <a data-value="5" onclick="setIndexErrorCat(this)" class="se-item">其他</a> </div> <span class="categorymsg text-danger"></span> </div> </div> <div class="form-group"> <label class="col-pre">反馈内容<span class="redstar">*</span></label> <div class="col-after"> <textarea class="form-control content" rows="5"  name="content" placeholder="亲爱的用户：请在这里直接填写您遇到的问题或意见建议，您的意见是我们前进的动力"></textarea> <span class="contentmsg text-danger"></span> </div> </div> <div class="form-group"> <label class="col-pre">手机号码<span class="redstar">*</span></label> <div class="col-after"> <input type="text" class="form-control phone" name="phone" placeholder="请输入手机号码，方便我们联系您。" value=""> <span class="phonemsg text-danger"></span> </div> </div> <div class="form-group"> <label class="col-pre">&nbsp;</label> <div class="col-after"> <span class="text-gray font-12">亲爱的顾客，您也可以直接拨打企查查官方电话：400-928-2212 或者 联系企查查官方客服QQ：4009985212，我们将及时为您解答问题。</span> </div> </div> </div> <div class="modal-footer"> <button type="button" class="btn btn-primary btn-guest">提交</button> </div> </form> <form class="pform-uploadimg" enctype="multipart/form-data" id="uploadVisitAddPic"> <input type="file" id="addVisitPic" name="pic"> </form> </div> </div> </div> <div style="display:none;"> <script src="https://s4.cnzz.com/z_stat.php?id=1254842228&web_id=1254842228" language="JavaScript"></script> <script>
      var _hmt = _hmt || [];
      (function() {
          var hm = document.createElement("script");
          hm.src = "https://hm.baidu.com/hm.js?3456bee468c83cc63fb5147f119f1075";
          var s = document.getElementsByTagName("script")[0];
          s.parentNode.insertBefore(hm, s);
      })();
  </script> <script>(function(){
          var src = (document.location.protocol == "http:") ? "http://js.passport.qihucdn.com/11.0.1.js?db135ad770b0860a90c3a2ca38cf577c":"https://jspassport.ssl.qhimg.com/11.0.1.js?db135ad770b0860a90c3a2ca38cf577c";
          document.write('<script src="' + src + '" id="sozz"><\/script>');
      })();
  </script> </div> <div class="modal fade" id="noteEditModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">编辑笔记</h4> </div> <div class="modal-body"> <form class="form-horizontal" role="form"> <div class="form-group"> <div class="col-sm-12"> <textarea class="form-control noteEditContent noteDetail" data-id="" rows="5" placeholder="亲爱的用户：请在这里填写您对该企业的笔记"></textarea> <span class="contentmsg text-danger"></span> </div> </div> <div class="form-group m-t-lg"> <div class="col-sm-12 text-center"> <span class="btn btn-primary  btn-block noteEditSubmit">提交</span> </div> </div> </form> </div> </div> </div> </div> <script type="text/javascript">
    function noteDetail(id){
        $.get(INDEX_URL+'/user_noteDetail', {id:id} ,function(result){
            if(result.success){
                $('.noteDetail').val(result.content);
                $('.noteDetail').attr('data-id',id);
            }
        });
    }

    //编辑笔记
    $('.noteEditSubmit').on('click',function(){
        var id = $(".noteEditContent").attr('data-id');
        var content = $.trim($(".noteEditContent").val());
        if(content==""){
            faldia({content:"请输入内容！"});
            return false;
        }
        $.ajax({
            type: 'POST',
            url:INDEX_URL+'/user_editNote',
            data:{id:id,content:content},
            success: function(result){
                if(result.success){
                    sucdia({content:"编辑成功！"});
                    $(".noteEditContent").val('');
                    window.location.reload();
                }else{
                    faldia({content:"编辑失败！"});
                }
            }
        });
    });
</script> <div class="modal fade" id="toDownloadModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal sm"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">提示</h4> </div> <div class="modal-body"> <p class="m-b-lg">您的报告正在生成中，请稍后前往<a target="_blank" href="/user_download">导出记录</a>下载。</p> </div> <div class="modal-footer"> <a rel="nofollow" href="/user_download" class="btn btn-primary pull-right">立即前往</a> </div> </div> </div> </div> <script type="text/javascript">
    (function(){
        var bp = document.createElement('script');
        var curProtocol = window.location.protocol.split(':')[0];
        if (curProtocol === 'https') {
            bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
        }
        else {
            bp.src = 'http://push.zhanzhang.baidu.com/push.js';
        }
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(bp, s);
    })();
</script> <link rel="stylesheet" type="text/css" href="/material/theme/chacha/cms/v2/css/rnav.css?timestamp=1573121164"> <div id="RNav" class="i_hide"> <div class="i_menu"> <ul class="i_bts-outer" style="bottom:69px;"> <li onclick="zhugeTrack('企业主页-对比企业',{'企业名称':'江苏华兰药用新材料股份有限公司'});" class="i_bt_lg i_bt_com i_to-option spanHide i_bt_xy" to="RNCom"> <i></i> <label>对比</label><span style="display: none;" id="ComCount">0</span></li> <li class="i_bt_sm i_bt_xcx"><i></i> <label>小程序</label><img src="/material/theme/chacha/cms/v2/images/leftnav/bg_xcx.png?t=2" alt="企查查"></li> <li class="i_bt_sm i_bt_wx"><i></i> <label>公众号</label><img src="/material/theme/chacha/cms/v2/images/leftnav/bg_wx.png?t=2" alt="企查查"></li> <li onclick="zhugeTrack('下载APP悬浮按钮');" class="i_bt_sm i_bt_dow"><i></i> <label>APP</label><img src="/material/theme/chacha/cms/v2/images/leftnav/bg_app.png?t=3" alt="企查查"></li> <script type="text/javascript" src="/material/js/jquery.cookie.js"></script> <script type="text/javascript" src="/material/js/jquery.validate.min.js"></script> <script type="text/javascript" src="/material/js/jquery.form.min.js"></script> <script type="text/javascript" src="/material/js/global.js?t=1573121164"></script> <li id="RNBack" class="i_bt_sm i_bt_kf" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()"><i></i> <label>反馈</label></li> <li class="i_bt_sm i_bt_back" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()"><i></i> <label>客服</label></li> <li id="RNTop" class="i_bt_sm i_bt_top"><i></i> <label>置顶</label></li> </ul> </div> <div class="i_container"> <div class="i_nodata">暂无数据</div> <div id="RNFoc" class="i_wrap"> <div class="i_title">我的关注</div> <div class="i_com-wrap"> <div style="height:1px;width:240px;"></div> </div> <div class="i_botbt"> <a href="/user_follow">打开全部</a> </div> </div> <div id="RNCom" class="i_wrap"> <div class="i_title">企业对比</div> <div class="i_toast">
				还可以添加<span id="ComLastCount">5</span>家企业 
				<a id="ClearCompares" class="c_a">清空</a> </div> <div class="i_com-wrap"> <div class="i_com i_addcom" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()"> <img src="/material/theme/chacha/cms/v2/images/leftnav/icon-add.png" alt="企查查"/> <a class="c_a" href="javascript:;">添加企业</a> </div> <div style="height:1px;width:240px;"></div> </div> <div class="i_botbt"> <a href="javascript:;" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">对比企业</a> </div> </div> <div id="RNRel" class="i_wrap"> <div class="i_title">找关系</div> <div class="i_toast">
				还可以添加<span id="RelLastCount">5</span>家企业 
				<a class="c_a" id="ClearRels">清空</a> </div> <div class="i_com-wrap"> <div class="i_com i_addcom" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()"> <img src="/material/theme/chacha/cms/v2/images/leftnav/icon-add.png" alt="企查查"/> <a class="c_a" href="javascript:;">添加企业或个人</a> </div> <div style="height:1px;width:240px;"></div> </div> <div class="i_botbt"> <a href="javascript:;" data-toggle="modal" data-target="#loginModal" onclick="getCaptcha()">找关系</a> </div> </div> </div> <div class="modal fade" id="qaddComPanel" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content" style="width:600px;"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">添加企业</h4> </div> <div class="modal-body" style="height: 330px"> <form class="form-horizontal" role="form"> <div class="form-group"> <div class="col-sm-12 m-t-md"> <input type="text" id="qcomName" name="comName" class="form-control" value="" placeholder="请输入公司/人" autocomplete="off" oninput="qsearchCom(event,this)"/> <section class="panel hidden-xs" id="qsearchList" style="position: absolute;width: 560px;z-index: 10;display: none;"></section> </div> <div class="col-sm-12 text-center m-t-lg" style="padding-left: 18px;padding-right: 18px;"> <span id="qaddComPanelConfirm" class="btn-primary btn-guest btn-block" style="padding-top: 5px;padding-bottom: 5px;cursor:pointer;">添加企业</span> </div> </div> </form> </div> </div> </div> </div> <div class="modal fade" id="addRelPanel" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content" style="width:600px;"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">添加企业或个人</h4> </div> <div class="modal-body" style="height: 445px"> <form class="form-horizontal" role="form"> <div class="form-group"> <div class="col-sm-12 m-t-md"> <input type="text" id="qrcomName" name="comName" class="form-control" value="" placeholder="请输入公司名称" autocomplete="off" oninput="qrsearchCom(event,this)"/> <section class="panel hidden-xs" id="qrsearchList" style="position: absolute;width: 560px;z-index: 10;display: none;"></section> </div> </div> </form> </div> </div> </div> </div> </div> <script type="text/javascript">
	 /*rightNav.js 使用变量*/
	 var personImg =  "/material/theme/chacha/cms/v2/images/leftnav/person.png";
	 var frimUrl = "";
	 var comDefaultImg = "/material/theme/chacha/cms/v2/images/company.jpg"
          
    function jumpTax(){
        window.location.href=encodeURI(INDEX_URL+"tax");
    }       
</script> <script src="/material/theme/chacha/cms/v2/js/rightNav.js?timestamp=1497542400"></script> <link type="text/css" href="/material/theme/chacha/cms/v2/css/login.css?version=1573121164" rel="stylesheet" /> <div class="modal fade" id="loginModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static"> <div class="modal-dialog login-madal-dialog"> <div class="modal-content"> <div class="modal-body"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <div class="login-sao-panel"> <div class="logo"> <img src="/material/theme/chacha/cms/v2/images/logo8.png"> </div> <div class="qrcodewrap"> <div class="qrcode" id='qrcodeModalLogin'></div> <img class="qrcodets" src="/material/theme/chacha/cms/v2/images/qrcode_ts.png?time=1573121164"> </div> <div class="title">扫码登录请使用<br> <a rel="nofollow" href="/app" target="_blank" class="text-primary">企查查APP</a> > 我的 > 扫一扫</div> </div> <div class="login-panel" style="display: none;" id="normalLoginPanel"> <div class="login-panel-head clearfix"> <div class="login-tab"> <a href="javascript:;" id="verifyLogin">快捷登录</a> </div> <div class="login-tab"> <a href="javascript:;" class="active">密码登录</a> </div> </div> <div class="login-panel-body"> <form class="form-group login-form" role="form" id="user_login_normal"> <div class="form-group"> <input type='hidden' class='phone_prefix_input' value="+86" name='phone_prefix' /> <div class="phone-select dropdown"> <a class="phone_prefix" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true"> 中国 +86<b class="caret text-primary"></b></a> <div class="phoneline"></div> <ul class="dropdown-menu"></ul> </div> <input id="nameNormal" name="nameNormal" type="text" class="form-control form-control-error" placeholder="请输入手机号码"> <span msgfor="nameNormal"></span> </div> <div class="form-group m-t-md"> <div class="show-pwd"></div> <input id="pwdNormal" name="pwdNormal" type="password" class="form-control form-control-error" placeholder="请输入密码"> <span msgfor="pwdNormal"></span> </div> <div class="form-group m-t-md"> <div id="dom_id_one"></div> </div> <div class="checkbox m-t-md" style="display: none;"> <label class="text-dark-lter"> <input type="checkbox" name="keep" checked="checked" value="option1"> 一周内保持登录状态
                                </label> </div> <button type="submit" class="btn btn-primary btn-block m-t-lg login-btn"> <strong>立即登录</strong></button> <input type='hidden' id='csessionid_one' name='csessionid_one' /> <input type='hidden' id='sig_one' name='sig_one' /> <input type='hidden' id='token_one' name='token_one' /> <input type='hidden' id='scene_one' name='scene_one' /> <input type='hidden' name='verify_type' value="1" /> </form> <div class="login-other m-t-md"> <div class="clearfix"> <div class="pull-left"> <a rel="nofollow" onclick="" href="/user_register" class="text-primary">免费注册</a> </div> <div class="pull-left text-dark-lt m-l-sm"> <a rel="nofollow" onclick="" href="/user_forgetpassword">忘记密码？</a> </div> <div class="pull-right"> <a rel="nofollow" href="https://open.weixin.qq.com/connect/qrconnect?appid=wx9b26295cdfab4175&redirect_uri=http://www.qichacha.com/user_wxloginok?back=&response_type=code&scope=snsapi_login&state=#wechat_redirect" class="btn-wx-d"></a> <a rel="nofollow" href="/user_qqlogin?back=&replace=1" class="btn-qq-d m-l-xs"> </a> <a rel="nofollow" href="/user_weiboLogin" class="btn-weibo-d m-l-xs"> </a> </div> </div> </div> </div> </div> <div class="login-panel" id="verifyLoginPanel"> <div class="login-panel-head clearfix"> <div class="login-tab"> <a href="javascript:;" class="active">快捷登录</a> </div> <div class="login-tab"> <a href="javascript:;" id="normalLogin">密码登录</a> </div> </div> <div class="login-panel-body"> <form class="form-group login-form" role="form" id="user_login_verify"> <div class="form-group"> <input type='hidden' class='phone_prefix_input' value="+86" name='phone_prefix' /> <div class="phone-select dropdown"> <a class="phone_prefix" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true"> 中国 +86<b class="caret text-primary"></b></a> <div class="phoneline"></div> <ul class="dropdown-menu"></ul> </div> <input id="nameVerify" name="nameVerify" onkeyup="phoneKeyup()" oninput="phoneKeyup()" type="text" class="form-control form-control-error" placeholder="请输入手机号码"> <span msgfor="nameVerify"></span> </div> <div class="form-group m-t-md"> <div id="dom_id_two"></div> </div> <div class="form-group m-t-md"> <input id="vcodeNormal" maxlength="6" name="codeVerify" type="text" class="form-control form-control-error" placeholder="短信验证码"> <a href="javascript:;" class="text-primary vcode-btn get-mobile-code">
                         获取验证码
                      </a> <span msgfor="codeVerify"> </span> </div> <div class="checkbox m-t-md" style="display: none;"> <label class="text-dark-lter"> <input type="checkbox" name="keep" checked="checked" value="option1"> 一周内保持登录状态
                                </label> </div> <button type="submit" class="btn btn-primary btn-block m-t-lg login-btn"> <strong>登录/注册</strong></button> <input type='hidden' id='csessionid_two' name='csessionid_two' /> <input type='hidden' id='sig_two' name='sig_two' /> <input type='hidden' id='token_two' name='token_two' /> <input type='hidden' id='scene_two' name='scene_two' /> </form> <div class="login-other m-t-md"> <div class="clearfix"> <div class="text-center text-gray m-b font-12">未注册的手机号或第三方账号验证后将自动创建新账号</div> <div class="text-center"> <a rel="nofollow" onclick="" href="https://open.weixin.qq.com/connect/qrconnect?appid=wx9b26295cdfab4175&redirect_uri=http://www.qichacha.com/user_wxloginok?back=&response_type=code&scope=snsapi_login&state=#wechat_redirect" class="btn-wx-d"></a> <a rel="nofollow" onclick="" href="/user_qqlogin?back=&replace=1" class="btn-qq-d m-l-xs"> </a> <a onclick="" routerLink="/user" class="btn-weibo-d m-l-xs"> </a> </div> </div> </div> </div> </div> </div> </div> </div> </div> <link type="text/css" href="//g.alicdn.com/sd/ncpc/nc.css?t=1520579483" rel="stylesheet" /> <script type="text/javascript" src="//g.alicdn.com/sd/ncpc/nc.js?t=1520579483"></script> <div id="_umfp" style="display:inline;width:1px;height:1px;overflow:hidden"></div> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/login.js?version=1573121164"></script> <script>

    //普通登录
    formset({
        "id":"user_login_normal",
        "url":"user_loginaction",
        "rule":{
            "nameNormal":{
                required:true,
            },
            "pwdNormal":{
                required:true,
                minlength:6
            }
        },

        "messages":{
            "nameNormal":{
                required:"请输入手机号",
            },
            "pwdNormal":{
                required:"请输入密码",
                minlength:"密码最少6位"
            }
        },
        "sucfunc":function(rs){
            $('#loginModalClose').click();
            location.reload();
        },
        "falfunc":function(rs){
            getAliCaptcha('one');
            document.getElementById('csessionid_one').value = '';
            document.getElementById('sig_one').value = '';
            document.getElementById('token_one').value = '';
            document.getElementById('scene_one').value = '';
            if(rs.msg=='手机号或密码错误'){
                $('span[msgfor=nameNormal]').show();
                $('span[msgfor=nameNormal]').html('<label id="nameNormal-error" class="validate-error">您输入的账号和密码不匹配，建议使用 <a class="text-primary" onclick="verifyLoginFuc()">验证码登录</a></label>');
            }else{
                faldia({'content':'登录失败：'+rs.msg});
            }
        }
    });
    //手机验证码登录
    formset({
        "id":"user_login_verify",
        "url":"user_loginbyverify",
        "rule":{
            "nameVerify":{
                required:true,
            },
            "codeVerify":{
                required:true,
                minlength:6
            }
        },

        "messages":{
            "nameVerify":{
                required:"请输入手机号",
            },
            "codeVerify":{
                required: "请输入手机激活码",
                minlength: "手机激活码最少{0}个字"
            }
        },
        "sucfunc":function(rs){
            $('#loginModalClose').click();
            location.reload();
        },
        "falfunc":function(rs){
            faldia({'content':'登录失败：'+rs.msg});
            getAliCaptcha('two');
            document.getElementById('csessionid_two').value = '';
            document.getElementById('sig_two').value = '';
            document.getElementById('token_two').value = '';
            document.getElementById('scene_two').value = '';
        }
    });

    var codeStatus = true;//状态
    var waitSec = 60; //设置秒数(单位秒)
    var i = 1;
    var clock;

    function sTimer() {
        var r = waitSec - i;
        if (r == 0) {
            clearInterval(clock);
            $(".get-mobile-code").html("重新获取");
            codeStatus = true;
            $(".get-mobile-code").data('clicked', false).removeClass('disabled');
        } else {
            $(".get-mobile-code").html("(" + r + ")秒重新发送");
            i++;
        }
    };
    function startClock(t) {
        codeStatus = false;
        i = parseInt(t);
        clock = setInterval(sTimer, 1000);
    }

    function phoneKeyup(){
      
    }

    

    //获取手机验证码
    function mobileCode() {
        $(".get-mobile-code").bind('click', function () {
            if ($(this).data('clicked')) return false;
            var phone = $("input[name=nameVerify]").val();
            var scene = $("input[name='scene_two']").val();
            var token = $("input[name='token_two']").val();
            var sig = $("input[name='sig_two']").val();
            var csessionid = $("input[name='csessionid_two']").val();
            var phone_prefix = $("#user_login_verify input[name='phone_prefix']").val();
            var afsFlag = '';

            if ($("input[name=nameVerify]").hasClass('validate-error')) {
                faldia('请重新输入手机号码！');
                return false;
            }

            if (!phone) {
                faldia('手机号码不能为空！');
                return false;
            }

            if(afsFlag){
                if(!scene || !token || !sig || !csessionid){
                    faldia('请先拖动滑块！');
                    return false;
                }
            }

            $.post(INDEX_URL + '/user_regmobileCode', {
                scene:scene,
                token:token,
                sig:sig,
                csessionid:csessionid,
                phone: phone,
                type: 4,
                verify_type:1,
                phone_prefix:phone_prefix
            }, function (data) {
                if (data.success) {
                    $("input[name=mobilecode]").removeAttr('disabled');
                    startClock(1);
                    $(".get-mobile-code").data('clicked', true).addClass('disabled').html("(" + waitSec + ")秒重新发送");
                } else {
                    faldia(data.msg);
                    getAliCaptcha('two');
                    $("input[name=mobilecode]").removeAttr('disabled');
                    $(".get-mobile-code").html("重新获取").data('clicked', false).removeClass('disabled');
                }
            }, 'json');
            return false;
        });
    }

    mobileCode();
</script> <script>

    function getCaptcha() {
        getAliCaptcha('two');

    }

    function getAliCaptcha(num){
        var renderDom = '#dom_id_'+num;
        var csessionidDom = 'csessionid_'+num;
        var sigDom = 'sig_'+num;
        var tokenDom = 'token_'+num;
        var sceneDom = 'scene_'+num;
        var nc = new noCaptcha();
        var nc_appkey = 'QNYX';  // 应用标识,不可更改
        var nc_scene = 'login';  //场景,不可更改
        var nc_token = [nc_appkey, (new Date()).getTime(), Math.random()].join(':');
        var nc_option = {
            renderTo: renderDom,
            appkey: nc_appkey,
            scene: nc_scene,
            token: nc_token,
            callback: function (data) {
                document.getElementById(csessionidDom).value = data.csessionid;
                document.getElementById(sigDom).value = data.sig;
                document.getElementById(tokenDom).value = nc_token;
                document.getElementById(sceneDom).value = nc_scene;
                if(num=='one'){
                    // if($("input[name=nameNormal]").val() && $("input[name=pwdNormal]").val()){
                    //     $('#user_login_normal').submit();
                    // }   
                }else if(num=='two'){
                    if($("input[name=nameVerify]").val()){
                        $(".get-mobile-code").trigger('click');
                    }
                }
            }
        };
        nc.init(nc_option);
    }

    function verifyLoginFuc(){
        $('#verifyLogin').trigger('click');
    }
    
    $('#verifyLogin').on('click',function(){
        getAliCaptcha('two');
        if($("input[name=nameNormal]").val()){
          $("input[name=nameVerify]").val($("input[name=nameNormal]").val());
        }else{
          setTimeout(function() {$("input[name=nameVerify]").focus();}, 10);
        }
        $('#verifyLoginPanel').show();
        $('#normalLoginPanel').hide();
        window.localStorage.setItem('logintype',0);
    });
    $('#normalLogin').on('click',function(){
        getAliCaptcha('one');
        if($("input[name=nameVerify]").val()){
          $("input[name=nameNormal]").val($("input[name=nameVerify]").val());
        }
        $('#normalLoginPanel').show();
        $('#verifyLoginPanel').hide();
        window.localStorage.setItem('logintype',1);
    });

    $('#normalLoginPanel .phone-select').phoneSelect();
    $('#verifyLoginPanel .phone-select').phoneSelect();
    
    $('.show-pwd').click(function(){
        if($('.show-pwd').hasClass('active')){
            $('.show-pwd').removeClass('active');
            $('.show-pwd').next().attr('type','password');
        }else{
            $('.show-pwd').addClass('active');
            $('.show-pwd').next().attr('type','text');
        }
    });
    var loginJumpUrl;
    $('#loginModal').on('show.bs.modal', function (e) {
        loginQrcodeGenerate('qrcodeModalLogin');
        loginQrcodePoll('qrcodeModalLogin');
    })
    $('#loginModal').on('hidden.bs.modal', function (e) {
        clearInterval(loginQrcodePollTimer);
    })
    setLoginType();

    function showLoginModal(){
        $('#loginModal').modal('show');
        getCaptcha();
    }
</script> <style type="text/css">


    .step2{display: none;}
</style> <link type="text/css" href="/material/theme/chacha/cms/v2/css/vip-modal.css?version=1573121164" rel="stylesheet"/> <div class="modal fade" id="vipModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="vip-top"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <div class="vip-title"> <div class="title">立即成为VIP</div> <div class="sub-title"><span>更多特权 超值服务</span><a rel="nofollow" href="/vip">全部特权></a></div> </div> <div class="vip-buy-panel"> <div class="vip-year-list clearfix"> <div data-id="17" data-year="3" data-price="720" class="vip-kuang vip-year active"> <div class="price"> <span>720元</span> <span class="vip-pay">/</span>
                                3年
                            </div> <div class="origin-price">原价：2160元</div> <div class="vip-rec"></div> </div> <div data-id="7" data-year="2" data-price="540" class="vip-kuang vip-year"> <div class="price"> <span>540元</span> <span class="vip-pay">/</span>
                                2年
                            </div> <div class="origin-price">原价：1440元</div> </div> <div data-id="6" data-year="1" data-price="360" class="vip-kuang vip-year"> <div class="price"> <span>360元</span> <span class="vip-pay">/</span>
                                1年
                            </div> <div class="origin-price">原价：720元</div> </div> </div> <div class="step1 m-t-md"> <a onclick="modalJumpVip()" class="vip-btn">立即开通</a> <div class="vip-publicity">支付后可开发票</div> </div> <form class="pay-form vip-pay-info step2" target="aliPayFrame" role="form" method="post" action="/order_pay"> <div class="clearfix"> <span class="pre">购买账号：</span><span class="after"></span> </div> <div class="clearfix coupon-drop" > <span class="pre">优惠券：</span><span  data-toggle="dropdown" class="after drop"><span class="couponText">暂无优惠券</span><span class="caret"></span></span> <ul class="dropdown-menu couponList"> <li> <span class="coupon-type">暂无优惠券</span> </li> </ul> </div> <div class="clearfix  m-b-xs"> <span class="pre">实付金额：</span><span class="after vip-pay payYear">¥720.00</span> </div> <input type="hidden" name="order_type" value="2"/> <input type="hidden" name="goods_id" value="17"/> <input type="hidden" name="pay_type" value="2"/> <input type="hidden" name="coupon_code" value=""/> <input type="submit" class="btn btn-primary packages-btn" value="立即支付" style="display: none"/> </form> </div> </div> <div class="vip-pay-container clearfix"> <div class="step1"> <img class="demo-img" src="/material/theme/chacha/cms/v2/images/vip/fxsm.png"/> <a class="vip-demo-link" href=""></a> </div> <div class="step2"> <div class="vip-payj-left"> <div onclick="checkPay(2)" class="pay-type pay-type-wx active"></div> <div onclick="checkPay(1)" class="pay-type pay-type-ali m-t-xs"></div> <div class="m-t-lg"> <p>1.完成支付后可在我的-我的发票中申请发票</p> <p>2.VIP会员自支付完成之时起5分钟内生效</p> </div> </div> <div class="vip-payj-qrcode"> <div class="wx_pay_box"> <div id="wx_pay_img" class="wx_pay_img"></div> <img class="pay-load" src="/material/theme/chacha/cms/v2/images/preloader.gif"> </div> <div class="ali_pay_box" loading-img="/material/theme/chacha/cms/v2/images/preloader.gif"> <img class="pay-load" src="/material/theme/chacha/cms/v2/images/preloader.gif"> </div> </div> </div> </div> </div> </div> </div> <div class="modal fade" id="svipModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal"> <div class="modal-content"> <div class="vip-top svip"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <div class="vip-title"> <div class="title">立即成为SVIP</div> <div class="sub-title"><span>更多特权 超值服务</span><a rel="nofollow" href="/vip_svip">全部特权></a></div> </div> <div class="vip-buy-panel"> <div class="vip-year-list clearfix"> <div data-id="33" data-year="3" data-price="3600" class="vip-kuang vip-year active"> <div class="price"> <span>3600元</span> <span class="vip-pay">/</span>
                                3年
                            </div> <div class="origin-price">原价：10800元</div> <div class="vip-rec"></div> </div> <div data-id="32" data-year="2" data-price="2700" class="vip-kuang vip-year"> <div class="price"> <span>2700元</span> <span class="vip-pay">/</span>
                                2年
                            </div> <div class="origin-price">原价：7200元</div> </div> <div data-id="31" data-year="1" data-price="1800" class="vip-kuang vip-year"> <div class="price"> <span>1800元</span> <span class="vip-pay">/</span>
                                1年
                            </div> <div class="origin-price">原价：3600元</div> </div> </div> <div class="step1 m-t-md"> <a onclick="modalJumpVip()" class="vip-btn">立即开通</a> <div class="vip-publicity">支付后可开发票</div> </div> <form class="pay-form vip-pay-info step2" target="aliPayFrameSVIP" role="form" method="post" action="/order_pay"> <div class="clearfix"> <span class="pre">购买账号：</span><span class="after"></span> </div> <div class="clearfix coupon-drop" > <span class="pre">优惠券：</span><span  data-toggle="dropdown" class="after drop"><span class="couponText">暂无优惠券</span><span class="caret"></span></span> <ul class="dropdown-menu couponList"> <li> <span class="coupon-type">暂无优惠券</span> </li> </ul> </div> <div class="clearfix m-b-xs" style="display: none;"> <span class="pre">原方案抵扣：</span><span class="after text-gray deduction">-￥1</span> </div> <div class="clearfix  m-b-xs"> <span class="pre">实付金额：</span><span class="after vip-pay payYear">¥3600.00</span> </div> <input type="hidden" name="order_type" value="7"/> <input type="hidden" name="goods_id" value="33"/> <input type="hidden" name="pay_type" value="2"/> <input type="hidden" name="coupon_code" value=""/> <input type="submit" class="btn btn-primary packages-btn" value="立即支付" style="display: none"/> </form> </div> </div> <div class="vip-pay-container clearfix"> <div class="step1"> <img class="demo-img" src="/material/theme/chacha/cms/v2/images/vip/fxsm.png"/> <a class="vip-demo-link" href=""></a> </div> <div class="step2"> <div class="vip-payj-left"> <div onclick="checkPay(2)" class="pay-type pay-type-wx active"></div> <div onclick="checkPay(1)" class="pay-type pay-type-ali m-t-xs"></div> <div class="m-t-lg"> <p>1.完成支付后可在我的-我的发票中申请发票</p> <p>2.支付完成之时起5分钟内生效</p> </div> </div> <div class="vip-payj-qrcode"> <div class="wx_pay_box"> <div id="wx_pay_img_svip" class="wx_pay_img"></div> <img class="pay-load" src="/material/theme/chacha/cms/v2/images/preloader.gif"> </div> <div class="ali_pay_box" loading-img="/material/theme/chacha/cms/v2/images/preloader.gif"> <img class="pay-load" src="/material/theme/chacha/cms/v2/images/preloader.gif"> </div> </div> </div> </div> </div> </div> </div> <script type="text/javascript" src="/material/theme/chacha/cms/v2/js/pay.js?time=1573121164"></script> <script type="text/javascript">
    var vipModalTitle;
    var userid = '';
    var $cmodal;

    var isPayShow = false;
    var wxOrderStatus = 0;
    var wxOrderCode = '';
    var wxpayLoad = false;
    var alipayLoad = false;
    var cPayType = 2;
    var isModalShow = true;
    var cGoods_id = "17";
    var cYear = "3";
    var cPrice = "720";
    var vType = 'vip';
    var cDeduction = 0;

    function showVipModal(title, subTitle, img, linkName, linkUrl, isStep2){
        if(img=='kzrt'){
            img='kzrt2';
        }
        if(!userid){
            getCaptcha();
            $('#loginModal').modal('show');
            return;
        }
        $cmodal = $("#vipModal");
        vType = 'vip';
        cGoods_id = "17";
        cYear = "3";
        cPrice = "720";

        $cmodal.find('.step1').show();
        $cmodal.find('.step2').hide();
        
        if(title){
             $cmodal.find('.vip-title .title').text(title);
            //vipModalTitle = title;
        }
        if(subTitle){
             $cmodal.find('.vip-title .sub-title span').text(subTitle);
        }
        if(img){
            if(title == '风险监控'){
                var imgUrl = "/material/theme/chacha/cms/v2/images/vip/fxsm2.png";
                 $cmodal.find(".demo-img").attr("src",imgUrl);
            } else {
                var imgUrl = "/material/theme/chacha/cms/v2/images/vip/"+img+".png";
                 $cmodal.find(".demo-img").attr("src",imgUrl);
            }
        } else {
            var imgUrl = "/material/theme/chacha/cms/v2/images/vip/default.png";
             $cmodal.find(".demo-img").attr("src",imgUrl);
        }
        if(linkName && linkUrl){
            $cmodal.find(".vip-demo-link").show();
            $cmodal.find(".vip-demo-link").text(linkName + '>');
            $cmodal.find(".vip-demo-link").attr('href',linkUrl);
        } else {
            $cmodal.find(".vip-demo-link").hide();
        }

        /*if(isStep2){
            $("#vipModal .step1").hide();
            $("#vipModal .step2").show();
            strartBuy();
        }*/

        $cmodal.modal('show');

        // 嵌入的关闭
        $(".vip-insert-wrap .step1").show();
        $(".vip-insert-wrap .step2").hide();
    }

    function showSVipModal(title, subTitle, img, linkName, linkUrl, isStep2){

        if(!userid){
            getCaptcha();
            $('#loginModal').modal('show');
            return;
        }
        $cmodal = $("#svipModal");
        vType = 'svip';
        cGoods_id = "33";
        cYear = "3";
        cPrice = "3600";
        
        $cmodal.find('.step1').show();
        $cmodal.find('.step2').hide();
        
        if(title){
             $cmodal.find('.vip-title .title').text(title);
            //vipModalTitle = title;
        }
        if(subTitle){
             $cmodal.find('.vip-title .sub-title span').text(subTitle);
        }
        if(img){
            if(title == '风险监控'){
                var imgUrl = "/material/theme/chacha/cms/v2/images/vip/ldjk.png";
                 $cmodal.find(".demo-img").attr("src",imgUrl);
            } else {
                var imgUrl = "/material/theme/chacha/cms/v2/images/vip/"+img+".png";
                 $cmodal.find(".demo-img").attr("src",imgUrl);
            }
        } else {
            var imgUrl = "/material/theme/chacha/cms/v2/images/vip/default.png";
             $cmodal.find(".demo-img").attr("src",imgUrl);
        }
        if(linkName && linkUrl){
            $cmodal.find(".vip-demo-link").show();
            $cmodal.find(".vip-demo-link").text(linkName + '>');
            $cmodal.find(".vip-demo-link").attr('href',linkUrl);
        } else {
            $cmodal.find(".vip-demo-link").hide();
        }

        /*if(isStep2){
            $("#vipModal .step1").hide();
            $("#vipModal .step2").show();
            strartBuy();
        }*/

        $cmodal.modal('show');

        // 嵌入的关闭
        $(".vip-insert-wrap .step1").show();
        $(".vip-insert-wrap .step2").hide();
    }

    $('#vipModal,#svipModal').on('hide.bs.modal',function(){
        clearPay();
        isPayShow = false;
    })

    $('#vipModal .vip-year-list .vip-kuang,#svipModal .vip-year-list .vip-kuang').on('click',function(){
        changeYear($(this).attr('data-id'),$(this).attr('data-year'),$(this).attr('data-price'),this);
        var couponCode = $cmodal.find("input[name='coupon_code']").val();
        if(couponCode == ''){
            //checkPay(cPayType);
        }
    });

    function modalJumpVip(){
        isPayShow = true;

        strartBuy();

        $cmodal.find('.step1').hide();
        $cmodal.find('.step2').show();
        zhugeTrack('开通VIP',{'立即开通点击来源':$cmodal.find('.vip-title .title').text()});
        /*
        location.href = INDEX_URL+'/vip?goods_id='+$("input[name='goods_id']").val();
        if(vipModalTitle){
            //zhugeTrack(vipModalTitle.split(' ')[0]+'-开通VIP');
        }else{
            //zhugeTrack('VIP弹框-开通VIP');
        }*/
    }
    

    var siModel = null;
    function strartBuy(){
        if(typeof siModel != 'undefined' && siModel){
            clearInterval(siModel);
            siModel = null;
        }
        if(typeof siInsert != 'undefined' && siInsert){
            clearInterval(siInsert);
            siInsert = null;
        }
        siModel = setInterval(function(){
            getWxPayStatus();
        }, 3000);
        //checkPay(cPayType);
        if(userGroupid==43){
            getdeduction();
        }
        setTimeout(function() {
            getcouponlist(cGoods_id);
            
        }, 500);
    }
</script> <style type="text/css"> </style> <div class="modal fade" id="confirmModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog nmodal ts-modal"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">x</span></button> <h4 class="modal-title">提示</h4> </div> <div class="modal-body clearfix"> <div class="title font-16 clearfix"> <div class="bd"> <span class="icon-warning"></span> </div> <div class="bd" style="padding-left: 10px;"> <span id="tkConfirmTitle">此操作永久删除，是否继续</span> </div> </div> <div class="btn-area m-t-md pull-right"> <a class="btn btn-default m-r-xs" data-dismiss="modal">取消</a> <a class="btn btn-primary" data-dismiss="modal" onclick="tkConfirmFuc()">确认删除</a> </div> </div> </div> </div> </div> <script type="text/javascript">
    var tkConfirmFuc;
    function tkConfirm(fuc,title) {
        $('#confirmModal').modal('show');
        tkConfirmFuc = fuc;
        if(title){
            $('#tkConfirmTitle').text(title);
        }else{
            $('#tkConfirmTitle').text('此操作永久删除，是否继续');
        }
    }
    function tkConfirmOk(){
        tkConfirmFuc();
    }
</script> <div id="openSuspend" class="openSuspend" style="cursor:pointer;"></div> <div class="bottomSuspend" id="bottomSuspend" style="margin-left: -100%;background-image: url('/material/theme/chacha/cms/v2/images/footer_app2_banner.png');"> <div id="attendDownload" class="attendDownload" data-href="https://www.qichacha.com/app?source=attendDownload"></div> <div id="closeSuspend" class="closeSuspend"></div> </div> <script type="text/javascript">
    bottomSus();
</script> </body> </html>
'NoneType' object has no attribute 'text'
{"name": "\u6c5f\u82cf\u534e\u5170\u836f\u7528\u65b0\u6750\u6599\u80a1\u4efd\u6709\u9650\u516c\u53f8"}
Process finished with exit code 0
'''