<template>
    <svg class="w-10 h-10 text-white icon" viewBox="0 0 52 52" fill="none">
        <path class="triangle" d="M26 8L46 42H6L26 8Z"/>

        <path class="line" d="M26 20V30"/>

        <circle class="dot" cx="26" cy="36" r="1.8"/>
    </svg>
</template>

<style scoped>
    .icon{
        animation:pulse .7s ease;
    }

    path, circle{
        stroke:currentColor;
        stroke-width:3;
        stroke-linecap:round;
        stroke-linejoin:round;
        fill:none;
    }

    .triangle{
        stroke-dasharray:120;
        stroke-dashoffset:120;
        animation:draw .6s forwards;
    }

    .line{
        stroke-dasharray:10;
        stroke-dashoffset:10;
        animation:draw .25s .5s forwards;
    }

    .dot{
        opacity:0;
        animation:show .2s .7s forwards;
    }

    @keyframes draw{
        to{
        stroke-dashoffset:0;
        }
    }

    @keyframes show{
        to{
        opacity:1;
        }
    }

    @keyframes pulse{
        0%{transform:scale(.8)}
        70%{transform:scale(1.08)}
        100%{transform:scale(1)}
    }
</style>